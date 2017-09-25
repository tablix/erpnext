// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on("Supplier", {
<<<<<<< HEAD
	setup: function (frm) {
		frm.set_query('default_price_list', { 'buying': 1 });
		frm.set_query('account', 'accounts', function (doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			return {
				filters: {
					'account_type': 'Payable',
					'company': d.company,
					"is_group": 0
				}
			}
		});
	},
	refresh: function (frm) {
		frappe.dynamic_link = { doc: frm.doc, fieldname: 'name', doctype: 'Supplier' }

		if (frappe.defaults.get_default("supp_master_name") != "Naming Series") {
=======
	before_load: function(frm) {
		frappe.setup_language_field(frm);
	},
	refresh: function(frm) {
		if(frappe.defaults.get_default("supp_master_name")!="Naming Series") {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			frm.toggle_display("naming_series", false);
		} else {
			erpnext.toggle_naming_series();
		}

<<<<<<< HEAD
		if (frm.doc.__islocal) {
			hide_field(['address_html','contact_html']);
			frappe.contacts.clear_address_and_contact(frm);
		}
		else {
			unhide_field(['address_html','contact_html']);
			frappe.contacts.render_address_and_contact(frm);

			// custom buttons
			frm.add_custom_button(__('Accounting Ledger'), function () {
				frappe.set_route('query-report', 'General Ledger',
					{ party_type: 'Supplier', party: frm.doc.name });
			});
			frm.add_custom_button(__('Accounts Payable'), function () {
				frappe.set_route('query-report', 'Accounts Payable', { supplier: frm.doc.name });
			});

			// indicators
			erpnext.utils.set_party_dashboard_indicators(frm);
		}
	},
});
=======
		if(frm.doc.__islocal){
	    	hide_field(['address_html','contact_html']);
			erpnext.utils.clear_address_and_contact(frm);
		}
		else {
		  	unhide_field(['address_html','contact_html']);
			erpnext.utils.render_address_and_contact(frm);
		}
	},
});

cur_frm.fields_dict['default_price_list'].get_query = function(doc, cdt, cdn) {
	return{
		filters:{'buying': 1}
	}
}

cur_frm.fields_dict['accounts'].grid.get_field('account').get_query = function(doc, cdt, cdn) {
	var d  = locals[cdt][cdn];
	return {
		filters: {
			'account_type': 'Payable',
			'company': d.company,
			"is_group": 0
		}
	}
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
