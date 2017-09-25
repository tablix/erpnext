// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt



frappe.ui.form.on_change("Installation Note", "customer",
	function(frm) { erpnext.utils.get_party_details(frm); });

frappe.ui.form.on_change("Installation Note", "customer_address",
	function(frm) { erpnext.utils.get_address_display(frm); });

frappe.ui.form.on_change("Installation Note", "contact_person",
	function(frm) { erpnext.utils.get_contact_details(frm); });

frappe.provide("erpnext.selling");
// TODO commonify this code
erpnext.selling.InstallationNote = frappe.ui.form.Controller.extend({
	onload: function() {
<<<<<<< HEAD
		if(!this.frm.doc.status) {
			set_multiple(this.frm.doc.doctype, this.frm.doc.name, { status:'Draft'});
		}
		if(this.frm.doc.__islocal) {
			set_multiple(this.frm.doc.doctype, this.frm.doc.name,
				{inst_date: frappe.datetime.get_today()});
		}
=======
		if(!this.frm.doc.status) set_multiple(dt,dn,{ status:'Draft'});
		if(this.frm.doc.__islocal) set_multiple(this.frm.doc.doctype, this.frm.doc.name,
				{inst_date: get_today()});
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

		this.setup_queries();
	},

	setup_queries: function() {
		var me = this;

<<<<<<< HEAD
		frappe.dynamic_link = {doc: this.frm.doc, fieldname: 'customer', doctype: 'Customer'}
		frm.set_query('customer_address', erpnext.queries.address_query);
		this.frm.set_query('contact_person', erpnext.queries.contact_query);
=======
		this.frm.set_query("customer_address", function() {
			return {
				filters: {'customer': me.frm.doc.customer }
			}
		});

		this.frm.set_query("contact_person", function() {
			return {
				filters: {'customer': me.frm.doc.customer }
			}
		});
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

		this.frm.set_query("customer", function() {
			return {
				query: "erpnext.controllers.queries.customer_query"
			}
		});
	},

	refresh: function() {
<<<<<<< HEAD
		var me = this;
		if (this.frm.doc.docstatus===0) {
			this.frm.add_custom_button(__('From Delivery Note'),
=======
		if (this.frm.doc.docstatus===0) {
			cur_frm.add_custom_button(__('From Delivery Note'),
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				function() {
					erpnext.utils.map_current_doc({
						method: "erpnext.stock.doctype.delivery_note.delivery_note.make_installation_note",
						source_doctype: "Delivery Note",
<<<<<<< HEAD
						target: me.frm,
						date_field: "posting_date",
						setters: {
							customer: me.frm.doc.customer || undefined,
						},
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
						get_query_filters: {
							docstatus: 1,
							status: ["not in", ["Stopped", "Closed"]],
							per_installed: ["<", 99.99],
<<<<<<< HEAD
							company: me.frm.doc.company
						}
					})
				}, "fa fa-download", "btn-default"
=======
							customer: cur_frm.doc.customer || undefined,
							company: cur_frm.doc.company
						}
					})
				}, "icon-download", "btn-default"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			);
		}
	},
});

$.extend(cur_frm.cscript, new erpnext.selling.InstallationNote({frm: cur_frm}));