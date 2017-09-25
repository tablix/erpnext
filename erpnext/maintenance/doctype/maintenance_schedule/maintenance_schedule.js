// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.maintenance");

<<<<<<< HEAD
frappe.ui.form.on('Maintenance Schedule', {
	setup: function(frm) {
		frm.set_query('contact_person', erpnext.queries.contact_query);
		frm.set_query('customer_address', erpnext.queries.address_query);
	},
	customer: function(frm) {
		erpnext.utils.get_party_details(frm)
	},
	customer_address: function(frm) {
		erpnext.utils.get_address_display(frm, 'customer_address', 'address_display');
	},
	contact_person: function(frm) {
		erpnext.utils.get_contact_details(frm);
	}

})
=======
frappe.ui.form.on_change("Maintenance Schedule", "customer", function(frm) {
	erpnext.utils.get_party_details(frm) });
frappe.ui.form.on_change("Maintenance Schedule", "customer_address", function(){
	erpnext.utils.get_address_display(cur_frm, 'customer_address', 'address_display');
});
frappe.ui.form.on_change("Maintenance Schedule", "contact_person", function(){
  erpnext.utils.get_contact_details(cur_frm);	
});
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

// TODO commonify this code
erpnext.maintenance.MaintenanceSchedule = frappe.ui.form.Controller.extend({
	refresh: function() {
<<<<<<< HEAD
		frappe.dynamic_link = {doc: this.frm.doc, fieldname: 'customer', doctype: 'Customer'}

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		var me = this;

		if (this.frm.doc.docstatus === 0) {
			this.frm.add_custom_button(__('Sales Order'),
				function() {
					erpnext.utils.map_current_doc({
						method: "erpnext.selling.doctype.sales_order.sales_order.make_maintenance_schedule",
						source_doctype: "Sales Order",
<<<<<<< HEAD
						target: me.frm,
						setters: {
							customer: me.frm.doc.customer || undefined
						},
						get_query_filters: {
							docstatus: 1,
=======
						get_query_filters: {
							docstatus: 1,
							order_type: me.frm.doc.order_type,
							customer: me.frm.doc.customer || undefined,
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
							company: me.frm.doc.company
						}
					});
				}, __("Get items from"));
		} else if (this.frm.doc.docstatus === 1) {
			this.frm.add_custom_button(__("Make Maintenance Visit"), function() {
				frappe.model.open_mapped_doc({
					method: "erpnext.maintenance.doctype.maintenance_schedule.maintenance_schedule.make_maintenance_visit",
					source_name: me.frm.doc.name,
					frm: me.frm
				})
			}, __("Make"));
		}
	},

	start_date: function(doc, cdt, cdn) {
		this.set_no_of_visits(doc, cdt, cdn);
	},

	end_date: function(doc, cdt, cdn) {
		this.set_no_of_visits(doc, cdt, cdn);
	},

	periodicity: function(doc, cdt, cdn) {
		this.set_no_of_visits(doc, cdt, cdn);
	},

	set_no_of_visits: function(doc, cdt, cdn) {
		var item = frappe.get_doc(cdt, cdn);

		if (item.start_date && item.end_date && item.periodicity) {
			if(item.start_date > item.end_date) {
<<<<<<< HEAD
				frappe.msgprint(__("Row {0}:Start Date must be before End Date", [item.idx]));
=======
				msgprint(__("Row {0}:Start Date must be before End Date", [item.idx]));
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				return;
			}

			var date_diff = frappe.datetime.get_diff(item.end_date, item.start_date) + 1;

			var days_in_period = {
				"Weekly": 7,
				"Monthly": 30,
				"Quarterly": 91,
				"Half Yearly": 182,
				"Yearly": 365
			}

			var no_of_visits = cint(date_diff / days_in_period[item.periodicity]);
			frappe.model.set_value(item.doctype, item.name, "no_of_visits", no_of_visits);
		}
	},
});

$.extend(cur_frm.cscript, new erpnext.maintenance.MaintenanceSchedule({frm: cur_frm}));

cur_frm.cscript.onload = function(doc, dt, dn) {
	if(!doc.status) set_multiple(dt,dn,{status:'Draft'});

	if(doc.__islocal){
<<<<<<< HEAD
		set_multiple(dt,dn,{transaction_date: frappe.datetime.get_today()});
=======
		set_multiple(dt,dn,{transaction_date:get_today()});
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	}

	// set add fetch for item_code's item_name and description
	cur_frm.add_fetch('item_code', 'item_name', 'item_name');
	cur_frm.add_fetch('item_code', 'description', 'description');

}

<<<<<<< HEAD
cur_frm.cscript.generate_schedule = function(doc, cdt, cdn) {
	if (!doc.__islocal) {
		return $c('runserverobj', {'method':'generate_schedule', 'docs':doc},
=======
cur_frm.fields_dict['customer_address'].get_query = function(doc, cdt, cdn) {
	return {
		filters:{ 'customer': doc.customer }
	}
}

cur_frm.fields_dict['contact_person'].get_query = function(doc, cdt, cdn) {
	return {
		filters:{ 'customer': doc.customer }
	}
}

cur_frm.cscript.generate_schedule = function(doc, cdt, cdn) {
	if (!doc.__islocal) {
		return $c('runserverobj', args={'method':'generate_schedule', 'docs':doc},
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			function(r, rt) {
				refresh_field('schedules');
			});
	} else {
<<<<<<< HEAD
		frappe.msgprint(__("Please save the document before generating maintenance schedule"));
=======
		msgprint(__("Please save the document before generating maintenance schedule"));
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	}
}

cur_frm.fields_dict.customer.get_query = function(doc,cdt,cdn) {
	return { query: "erpnext.controllers.queries.customer_query" }
}
