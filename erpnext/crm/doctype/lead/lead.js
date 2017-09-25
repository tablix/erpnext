// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext");
cur_frm.email_field = "email_id";

erpnext.LeadController = frappe.ui.form.Controller.extend({
	setup: function() {
		this.frm.fields_dict.customer.get_query = function(doc, cdt, cdn) {
<<<<<<< HEAD
			return { query: "erpnext.controllers.queries.customer_query" } }
=======
				return { query: "erpnext.controllers.queries.customer_query" } }
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	},

	onload: function() {
		if(cur_frm.fields_dict.lead_owner.df.options.match(/^User/)) {
			cur_frm.fields_dict.lead_owner.get_query = function(doc, cdt, cdn) {
<<<<<<< HEAD
				return { query: "frappe.core.doctype.user.user.user_query" }
			}
=======
				return { query:"frappe.core.doctype.user.user.user_query" } }
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		}

		if(cur_frm.fields_dict.contact_by.df.options.match(/^User/)) {
			cur_frm.fields_dict.contact_by.get_query = function(doc, cdt, cdn) {
<<<<<<< HEAD
				return { query: "frappe.core.doctype.user.user.user_query" } }
=======
				return { query:"frappe.core.doctype.user.user.user_query" } }
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		}
	},

	refresh: function() {
		var doc = this.frm.doc;
		erpnext.toggle_naming_series();
<<<<<<< HEAD
		frappe.dynamic_link = {doc: doc, fieldname: 'name', doctype: 'Lead'}

		if(!doc.__islocal && doc.__onload && !doc.__onload.is_customer) {
			this.frm.add_custom_button(__("Customer"), this.create_customer, __("Make"));
			this.frm.add_custom_button(__("Opportunity"), this.create_opportunity, __("Make"));
			this.frm.add_custom_button(__("Quotation"), this.make_quotation, __("Make"));
=======

		if(!this.frm.doc.__islocal && this.frm.doc.__onload && !this.frm.doc.__onload.is_customer) {
			this.frm.add_custom_button(__("Customer"), this.create_customer, __("Make"));
			this.frm.add_custom_button(__("Opportunity"), this.create_opportunity, __("Make"));
			this.frm.add_custom_button(__("Quotation"), this.make_quotation, __("Make"));
			this.frm.add_custom_button(__("Contact"), this.make_contact, __("Make"));
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}

		if(!this.frm.doc.__islocal) {
<<<<<<< HEAD
			frappe.contacts.render_address_and_contact(cur_frm);
		} else {
			frappe.contacts.clear_address_and_contact(cur_frm);
=======
			erpnext.utils.render_address_and_contact(cur_frm);
		} else {
			erpnext.utils.clear_address_and_contact(cur_frm);
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		}
	},

	create_customer: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.crm.doctype.lead.lead.make_customer",
			frm: cur_frm
		})
	},

	create_opportunity: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.crm.doctype.lead.lead.make_opportunity",
			frm: cur_frm
		})
	},

	make_quotation: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.crm.doctype.lead.lead.make_quotation",
			frm: cur_frm
		})
<<<<<<< HEAD
=======
	},
	make_contact: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.crm.doctype.lead.lead.make_contact",
			frm: cur_frm
		})
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	}
});

$.extend(cur_frm.cscript, new erpnext.LeadController({frm: cur_frm}));



