// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

cur_frm.cscript.tax_table = "Purchase Taxes and Charges";

{% include "erpnext/public/js/controllers/accounts.js" %}

frappe.ui.form.on("Purchase Taxes and Charges", "add_deduct_tax", function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];

	if(!d.category && d.add_deduct_tax) {
<<<<<<< HEAD
		frappe.msgprint(__("Please select Category first"));
		d.add_deduct_tax = '';
	}
	else if(d.category != 'Total' && d.add_deduct_tax == 'Deduct') {
		frappe.msgprint(__("Cannot deduct when category is for 'Valuation' or 'Valuation and Total'"));
=======
		msgprint(__("Please select Category first"));
		d.add_deduct_tax = '';
	}
	else if(d.category != 'Total' && d.add_deduct_tax == 'Deduct') {
		msgprint(__("Cannot deduct when category is for 'Valuation' or 'Valuation and Total'"));
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		d.add_deduct_tax = '';
	}
	refresh_field('add_deduct_tax', d.name, 'taxes');
});

frappe.ui.form.on("Purchase Taxes and Charges", "category", function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];

	if (d.category != 'Total' && d.add_deduct_tax == 'Deduct') {
<<<<<<< HEAD
		frappe.msgprint(__("Cannot deduct when category is for 'Valuation' or 'Vaulation and Total'"));
=======
		msgprint(__("Cannot deduct when category is for 'Valuation' or 'Vaulation and Total'"));
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		d.add_deduct_tax = '';
	}
	refresh_field('add_deduct_tax', d.name, 'taxes');
});
