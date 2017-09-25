// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Asset Movement', {
	onload: function(frm) {
		frm.add_fetch("asset", "warehouse", "source_warehouse");
<<<<<<< HEAD

=======
		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		frm.set_query("target_warehouse", function() {
			return {
				filters: [
					["Warehouse", "company", "in", ["", cstr(frm.doc.company)]],
					["Warehouse", "is_group", "=", 0]
				]
			}
		})

	}
});
