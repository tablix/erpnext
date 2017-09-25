// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.offer_letter");

frappe.ui.form.on("Offer Letter", {
<<<<<<< HEAD
	select_terms: function (frm) {
		erpnext.utils.get_terms(frm.doc.select_terms, frm.doc, function (r) {
			if (!r.exc) {
				frm.set_value("terms", r.message);
			}
		});
	},

	refresh: function (frm) {
		if ((!frm.doc.__islocal) && (frm.doc.status == 'Accepted') && (frm.doc.docstatus === 1)) {
			frm.add_custom_button(__('Make Employee'),
				function () {
=======
	select_terms: function(frm) {
		frappe.model.get_value("Terms and Conditions", frm.doc.select_terms, "terms", function(value) {
			frm.set_value("terms", value.terms);
		});
	},

	refresh:function(frm){
		if((!frm.doc.__islocal) && (frm.doc.status=='Accepted') && (frm.doc.docstatus===1)){
			frm.add_custom_button(__('Make Employee'),
				function() {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
					erpnext.offer_letter.make_employee(frm)
				}
			);
		}
	}

});

<<<<<<< HEAD
erpnext.offer_letter.make_employee = function (frm) {
=======
erpnext.offer_letter.make_employee = function(frm) {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	frappe.model.open_mapped_doc({
		method: "erpnext.hr.doctype.offer_letter.offer_letter.make_employee",
		frm: frm
	});
};
