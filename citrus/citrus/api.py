import frappe

@frappe.whitelist()
def send_email(email_to, item):
    if not email_to:
        email_to = frappe.session.user
        
    sales_invoices = frappe.db.sql(
        """
        SELECT
            tsi.name,
            tsi.posting_date
        FROM
            `tabSales Invoice Item` tsii
        INNER JOIN `tabSales Invoice` tsi ON
            tsi.name = tsii.parent
            AND tsi.docstatus = 1
        WHERE
            tsii.item_code = %s
        GROUP BY
            tsi.name
        ORDER BY
            tsi.name DESC
        LIMIT 5
        """, (item), as_dict=True
    )
    
    attachments = []
    for invoice in sales_invoices:
        doc = frappe.get_doc("Sales Invoice", invoice)
        attachments.append(
            frappe.attach_print(
                doc.doctype,
                doc.name,
                doc=doc,
                print_format="Standard"
            )
        )
        
    subject = f"Sales Invoice for Item - {item}"
    
    template = frappe.get_doc("Email Template", "Sales Invoice")
    
    message = frappe.render_template(template.response_html, {"sales_invoices": sales_invoices})
        
    frappe.sendmail(recipients=["test@example.com"], subject=subject, attachments=attachments, message=message)
    
    frappe.msgprint("Email Sent Successfully", alert=True)