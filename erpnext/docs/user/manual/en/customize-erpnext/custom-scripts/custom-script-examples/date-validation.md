# Date Validation


	frappe.ui.form.on("Task", "validate", function(frm) {
        if (frm.doc.from_date < get_today()) {
<<<<<<< HEAD
            frappe.msgprint(__("You can not select past date in From Date"));
            frappe.validated = false;
=======
            msgprint(__("You can not select past date in From Date"));
            validated = false;
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
        }
	});

{next}
