frappe.ui.form.on('Item', {
    refresh(frm) {
        frm.add_custom_button(__('Send Email'), () => {
            frappe.prompt({
                label: __('To'),
				fieldname: "email_to",
				fieldtype: "Data",
            },
            (values) => {
                frappe.call({
                    method: 'citrus.citrus.api.send_email',
                    args: {
                        email_to: values.email_to || '',
                        item: frm.doc.name
                    }
                })
            }
            )
        }, __('Actions'))
    }
})