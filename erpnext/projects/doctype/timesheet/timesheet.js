// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt
<<<<<<< HEAD

frappe.ui.form.on("Timesheet", {
	setup: function(frm) {
		frm.add_fetch('employee', 'employee_name', 'employee_name');
=======
cur_frm.add_fetch('employee', 'employee_name', 'employee_name');

frappe.ui.form.on("Timesheet", {
	setup: function(frm) {
		frm.get_field('time_logs').grid.editable_fields = [
			{fieldname: 'activity_type', columns: 2},
			{fieldname: 'from_time', columns: 2},
			{fieldname: 'to_time', columns: 2},
			{fieldname: 'hours', columns: 1},
			{fieldname: 'task', columns: 1},
			{fieldname: 'remark', columns: 2},
		];

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		frm.fields_dict.employee.get_query = function() {
			return {
				filters:{
					'status': 'Active'
				}
			}
		}

		frm.fields_dict['time_logs'].grid.get_field('task').get_query = function(frm, cdt, cdn) {
<<<<<<< HEAD
			var child = locals[cdt][cdn];
=======
			child = locals[cdt][cdn];
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			return{
				filters: {
					'project': child.project,
					'status': ["!=", "Closed"]
				}
			}
		}
<<<<<<< HEAD

		frm.fields_dict['time_logs'].grid.get_field('project').get_query = function() {
			return{
				filters: {
					'company': frm.doc.company
				}
			}
		}
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	},

	onload: function(frm){
		if (frm.doc.__islocal && frm.doc.time_logs) {
			calculate_time_and_amount(frm);
		}
	},

	refresh: function(frm) {
		if(frm.doc.docstatus==1) {
<<<<<<< HEAD
			if(frm.doc.per_billed < 100){
				frm.add_custom_button(__("Make Sales Invoice"), function() { frm.trigger("make_invoice") },
					"fa fa-file-alt");
=======
			if(!frm.doc.sales_invoice && frm.doc.total_billing_amount > 0){
				frm.add_custom_button(__("Make Sales Invoice"), function() { frm.trigger("make_invoice") },
					"icon-file-alt");
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			}

			if(!frm.doc.salary_slip && frm.doc.employee){
				frm.add_custom_button(__("Make Salary Slip"), function() { frm.trigger("make_salary_slip") },
<<<<<<< HEAD
					"fa fa-file-alt");
			}
		}

		if(frm.doc.per_billed > 0) {
			frm.fields_dict["time_logs"].grid.toggle_enable("billing_hours", false);
			frm.fields_dict["time_logs"].grid.toggle_enable("billable", false);
		}
	},

	make_invoice: function(frm) {
		let dialog = new frappe.ui.Dialog({
			title: __("Select Item (optional)"),
			fields: [
				{"fieldtype": "Link", "label": __("Item Code"), "fieldname": "item_code", "options":"Item"},
				{"fieldtype": "Link", "label": __("Customer"), "fieldname": "customer", "options":"Customer"}
			]
		});

		dialog.set_primary_action(__("Make Sales Invoice"), () => {
			var args = dialog.get_values();
			if(!args) return;
			dialog.hide();
			return frappe.call({
				type: "GET",
				method: "erpnext.projects.doctype.timesheet.timesheet.make_sales_invoice",
				args: {
					"source_name": frm.doc.name,
					"item_code": args.item_code,
					"customer": args.customer
				},
				freeze: true,
				callback: function(r) {
					if(!r.exc) {
						frappe.model.sync(r.message);
						frappe.set_route("Form", r.message.doctype, r.message.name);
					}
				}
			})
		})

		dialog.show();
=======
					"icon-file-alt");
			}
		}
	},

	make_invoice: function(frm) {
		frappe.model.open_mapped_doc({
			method: "erpnext.projects.doctype.timesheet.timesheet.make_sales_invoice",
			frm: frm
		});
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	},

	make_salary_slip: function(frm) {
		frappe.model.open_mapped_doc({
			method: "erpnext.projects.doctype.timesheet.timesheet.make_salary_slip",
			frm: frm
		});
	},
})

frappe.ui.form.on("Timesheet Detail", {
	time_logs_remove: function(frm) {
		calculate_time_and_amount(frm);
	},

	from_time: function(frm, cdt, cdn) {
<<<<<<< HEAD
		calculate_end_time(frm, cdt, cdn);
=======
		calculate_end_time(frm, cdt, cdn)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	},

	to_time: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];

		if(frm._setting_hours) return;
		frappe.model.set_value(cdt, cdn, "hours", moment(child.to_time).diff(moment(child.from_time),
			"seconds") / 3600);
	},

	hours: function(frm, cdt, cdn) {
		calculate_end_time(frm, cdt, cdn)
	},

<<<<<<< HEAD
	billing_hours: function(frm, cdt, cdn) {
		calculate_billing_costing_amount(frm, cdt, cdn)
	},

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	billing_rate: function(frm, cdt, cdn) {
		calculate_billing_costing_amount(frm, cdt, cdn)
	},

	costing_rate: function(frm, cdt, cdn) {
		calculate_billing_costing_amount(frm, cdt, cdn)
	},

	billable: function(frm, cdt, cdn) {
<<<<<<< HEAD
		update_billing_hours(frm, cdt, cdn);
		update_time_rates(frm, cdt, cdn);
		calculate_billing_costing_amount(frm, cdt, cdn);
	},

	activity_type: function(frm, cdt, cdn) {
		frm.script_manager.copy_from_first_row('time_logs', frm.selected_doc,
			'project');

=======
		calculate_billing_costing_amount(frm, cdt, cdn)
	},

	activity_type: function(frm, cdt, cdn) {
		child = locals[cdt][cdn];
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		frappe.call({
			method: "erpnext.projects.doctype.timesheet.timesheet.get_activity_cost",
			args: {
				employee: frm.doc.employee,
<<<<<<< HEAD
				activity_type: frm.selected_doc.activity_type
=======
				activity_type: child.activity_type
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			},
			callback: function(r){
				if(r.message){
					frappe.model.set_value(cdt, cdn, 'billing_rate', r.message['billing_rate']);
					frappe.model.set_value(cdt, cdn, 'costing_rate', r.message['costing_rate']);
<<<<<<< HEAD
					calculate_billing_costing_amount(frm, cdt, cdn);
=======
					calculate_billing_costing_amount(frm, cdt, cdn)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				}
			}
		})
	}
});

<<<<<<< HEAD
var calculate_end_time = function(frm, cdt, cdn) {
	var child = locals[cdt][cdn];

	var d = moment(child.from_time);
	if(child.hours) {
		d.add(child.hours, "hours");
		frm._setting_hours = true;
		frappe.model.set_value(cdt, cdn, "to_time",
			d.format(moment.defaultDatetimeFormat)).then(() => {
				frm._setting_hours = false;
			});
	}


	if((frm.doc.__islocal || frm.doc.__onload.maintain_bill_work_hours_same) && child.hours){
		frappe.model.set_value(cdt, cdn, "billing_hours", child.hours);
	}
}

var update_billing_hours = function(frm, cdt, cdn){
	var child = locals[cdt][cdn];
	if(!child.billable) frappe.model.set_value(cdt, cdn, 'billing_hours', 0.0);
}

var update_time_rates = function(frm, cdt, cdn){
	var child = locals[cdt][cdn];
	if(!child.billable){
		frappe.model.set_value(cdt, cdn, 'billing_rate', 0.0);
		frappe.model.set_value(cdt, cdn, 'costing_rate', 0.0);
	}
}

var calculate_billing_costing_amount = function(frm, cdt, cdn){
	var child = locals[cdt][cdn];
	var billing_amount = 0.0;
	var costing_amount = 0.0;

	if(child.billing_hours && child.billable){
		billing_amount = (child.billing_hours * child.billing_rate);
		costing_amount = flt(child.costing_rate * child.billing_hours);
=======
calculate_end_time = function(frm, cdt, cdn){
	var child = locals[cdt][cdn];

	var d = moment(child.from_time);
	d.add(child.hours, "hours");
	frm._setting_hours = true;
	frappe.model.set_value(cdt, cdn, "to_time", d.format(moment.defaultDatetimeFormat));
	frm._setting_hours = false;

	calculate_billing_costing_amount(frm, cdt, cdn)
}

var calculate_billing_costing_amount = function(frm, cdt, cdn){
	child = locals[cdt][cdn]
	billing_amount = costing_amount = 0.0;

	if(child.hours && child.billable){
		billing_amount = (child.hours * child.billing_rate);
		costing_amount = flt(child.costing_rate * child.hours);
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	}

	frappe.model.set_value(cdt, cdn, 'billing_amount', billing_amount);
	frappe.model.set_value(cdt, cdn, 'costing_amount', costing_amount);
<<<<<<< HEAD
	calculate_time_and_amount(frm);
=======
	calculate_time_and_amount(frm)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
}

var calculate_time_and_amount = function(frm) {
	var tl = frm.doc.time_logs || [];
<<<<<<< HEAD
	var total_working_hr = 0;
	var total_billing_hr = 0;
	var total_billable_amount = 0;
	var total_costing_amount = 0;
	for(var i=0; i<tl.length; i++) {
		if (tl[i].hours) {
			total_working_hr += tl[i].hours;
			total_billable_amount += tl[i].billing_amount;
			total_costing_amount += tl[i].costing_amount;

			if(tl[i].billable){
				total_billing_hr += tl[i].billing_hours;
			}
		}
	}

	frm.set_value("total_billable_hours", total_billing_hr);
	frm.set_value("total_hours", total_working_hr);
	frm.set_value("total_billable_amount", total_billable_amount);
	frm.set_value("total_costing_amount", total_costing_amount);
=======
	total_hr = 0;
	total_billing_amount = 0;
	total_costing_amount = 0;
	for(var i=0; i<tl.length; i++) {
		if (tl[i].hours) {
			total_hr += tl[i].hours;
			total_billing_amount += tl[i].billing_amount;
			total_costing_amount += tl[i].costing_amount;
		}
	}

	cur_frm.set_value("total_hours", total_hr);
	cur_frm.set_value("total_billing_amount", total_billing_amount);
	cur_frm.set_value("total_costing_amount", total_costing_amount);
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
}