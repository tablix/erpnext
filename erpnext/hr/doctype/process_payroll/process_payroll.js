// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

<<<<<<< HEAD
var in_progress = false;

frappe.ui.form.on("Process Payroll", {
	onload: function (frm) {
		frm.doc.posting_date = frappe.datetime.nowdate();
		frm.doc.start_date = '';
		frm.doc.end_date = '';
		frm.doc.payroll_frequency = '';
		frm.toggle_reqd(['payroll_frequency'], !frm.doc.salary_slip_based_on_timesheet);
	},

	setup: function (frm) {
		frm.set_query("payment_account", function () {
			var account_types = ["Bank", "Cash"];
			return {
				filters: {
					"account_type": ["in", account_types],
					"is_group": 0,
					"company": frm.doc.company
				}
			}
		}),
			frm.set_query("cost_center", function () {
				return {
					filters: {
						"is_group": 0,
						company: frm.doc.company
					}
				}
			}),
			frm.set_query("project", function () {
				return {
					filters: {
						company: frm.doc.company
					}
				}
			})
	},

	refresh: function (frm) {
		frm.disable_save();
	},

	payroll_frequency: function (frm) {
		frm.trigger("set_start_end_dates");
	},

	start_date: function (frm) {
		if(!in_progress && frm.doc.start_date){
			frm.trigger("set_end_date");
		}else{
			// reset flag
			in_progress = false
		}
	},

	salary_slip_based_on_timesheet: function (frm) {
		frm.toggle_reqd(['payroll_frequency'], !frm.doc.salary_slip_based_on_timesheet);
	},

	payment_account: function (frm) {
		frm.toggle_display(['make_bank_entry'], (frm.doc.payment_account != "" && frm.doc.payment_account != "undefined"));
	},

	set_start_end_dates: function (frm) {
		if (!frm.doc.salary_slip_based_on_timesheet) {
			frappe.call({
				method: 'erpnext.hr.doctype.process_payroll.process_payroll.get_start_end_dates',
				args: {
					payroll_frequency: frm.doc.payroll_frequency,
					start_date: frm.doc.posting_date
				},
				callback: function (r) {
					if (r.message) {
						in_progress = true;
						frm.set_value('start_date', r.message.start_date);
						frm.set_value('end_date', r.message.end_date);
					}
				}
			})
		}
	},

	set_end_date: function(frm){
		frappe.call({
			method: 'erpnext.hr.doctype.process_payroll.process_payroll.get_end_date',
			args: {
				frequency: frm.doc.payroll_frequency,
				start_date: frm.doc.start_date
			},
			callback: function (r) {
				if (r.message) {
					frm.set_value('end_date', r.message.end_date);
				}
			}
		})
	}
})

cur_frm.cscript.display_activity_log = function (msg) {
	if (!cur_frm.ss_html)
		cur_frm.ss_html = $a(cur_frm.fields_dict['activity_log'].wrapper, 'div');
	if (msg) {
		cur_frm.ss_html.innerHTML =
			'<div class="padding"><h4>' + __("Activity Log:") + '</h4>' + msg + '</div>';
=======
cur_frm.cscript.display_activity_log = function(msg) {
	if(!cur_frm.ss_html)
		cur_frm.ss_html = $a(cur_frm.fields_dict['activity_log'].wrapper,'div');
	if(msg) {
		cur_frm.ss_html.innerHTML =
			'<div class="padding"><h4>'+__("Activity Log:")+'</h4>'+msg+'</div>';
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	} else {
		cur_frm.ss_html.innerHTML = "";
	}
}

<<<<<<< HEAD
// Create salary slip
// -----------------------
cur_frm.cscript.create_salary_slip = function (doc, cdt, cdn) {
	cur_frm.cscript.display_activity_log("");
	var callback = function (r, rt) {
		if (r.message)
			cur_frm.cscript.display_activity_log(r.message);
	}
	return $c('runserverobj', { 'method': 'create_salary_slips', 'docs': doc }, callback);
}

cur_frm.cscript.submit_salary_slip = function (doc, cdt, cdn) {
	cur_frm.cscript.display_activity_log("");

	frappe.confirm(__("Do you really want to Submit all Salary Slip from {0} to {1}", [doc.start_date, doc.end_date]), function () {
		// clear all in locals
		if (locals["Salary Slip"]) {
			$.each(locals["Salary Slip"], function (name, d) {
=======
//Create salary slip
//-----------------------
cur_frm.cscript.create_salary_slip = function(doc, cdt, cdn) {
	cur_frm.cscript.display_activity_log("");
	var callback = function(r, rt){
		if (r.message)
			cur_frm.cscript.display_activity_log(r.message);
	}
	return $c('runserverobj', args={'method':'create_sal_slip','docs':doc},callback);
}

cur_frm.cscript.submit_salary_slip = function(doc, cdt, cdn) {
	cur_frm.cscript.display_activity_log("");

	frappe.confirm(__("Do you really want to Submit all Salary Slip for month {0} and year {1}", [doc.month, doc.fiscal_year]), function() {
		// clear all in locals
		if(locals["Salary Slip"]) {
			$.each(locals["Salary Slip"], function(name, d) {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				frappe.model.remove_from_locals("Salary Slip", name);
			});
		}

<<<<<<< HEAD
		var callback = function (r, rt) {
=======
		var callback = function(r, rt){
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			if (r.message)
				cur_frm.cscript.display_activity_log(r.message);
		}

<<<<<<< HEAD
		return $c('runserverobj', { 'method': 'submit_salary_slips', 'docs': doc }, callback);
	});
}

cur_frm.cscript.make_bank_entry = function (doc, cdt, cdn) {
	if (doc.company && doc.start_date && doc.end_date) {
		return frappe.call({
			doc: cur_frm.doc,
			method: "make_payment_entry",
			callback: function (r) {
				if (r.message)
					var doc = frappe.model.sync(r.message)[0];
				frappe.set_route("Form", doc.doctype, doc.name);
			}
		});
	} else {
		frappe.msgprint(__("Company, From Date and To Date is mandatory"));
	}
}
=======
		return $c('runserverobj', args={'method':'submit_salary_slip','docs':doc},callback);
	});
}

cur_frm.cscript.make_bank_entry = function(doc,cdt,cdn){
    if(doc.company && doc.month && doc.fiscal_year){
    	cur_frm.cscript.make_jv(doc, cdt, cdn);
    } else {
  	  msgprint(__("Company, Month and Fiscal Year is mandatory"));
    }
}

cur_frm.cscript.make_jv = function(doc, dt, dn) {
	return $c_obj(doc, 'make_journal_entry', '', function(r) {
		var doc = frappe.model.sync(r.message)[0];
		frappe.set_route("Form", doc.doctype, doc.name);
	});
}

frappe.ui.form.on("Process Payroll", {
	refresh: function(frm) {
		frm.disable_save();
	}
})
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
