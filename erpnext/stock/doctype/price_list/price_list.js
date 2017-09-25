// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

<<<<<<< HEAD
frappe.ui.form.on("Price List", {
	refresh: function(frm) {
		let me = this;
		frm.add_custom_button(__("Add / Edit Prices"), function() {
			frappe.route_options = {
				"price_list": frm.doc.name
			};
			frappe.set_route("Report", "Item Price");
		}, "fa fa-money");
	}
});
=======
$.extend(cur_frm.cscript, {
	refresh: function() {
		cur_frm.add_custom_button(__("Add / Edit Prices"), function() {
			frappe.route_options = {
				"price_list": cur_frm.doc.name
			};
			frappe.set_route("Report", "Item Price");
		}, "icon-money");
	}
});
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
