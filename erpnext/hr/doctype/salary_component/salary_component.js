// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Salary Component', {
<<<<<<< HEAD
	setup: function(frm) {
		frm.set_query("default_account", "accounts", function(doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			var root_types = ["Expense", "Liability"];
			return {
				filters: {
					"root_type": ["in", root_types],
					"is_group": 0,
					"company": d.company
				}
			}
		})
	}
});
=======
	refresh: function(frm) {

	}
});
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
