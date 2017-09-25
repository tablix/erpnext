// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

cur_frm.add_fetch('employee', 'company', 'company');
cur_frm.add_fetch('time_sheet', 'total_hours', 'working_hours');

frappe.ui.form.on("Salary Slip", {
	setup: function(frm) {
		frm.fields_dict["timesheets"].grid.get_field("time_sheet").get_query = function(){
			return {
				filters: {
					employee: frm.doc.employee
				}
			}
		}
<<<<<<< HEAD
		frm.set_query("salary_component", "earnings", function() {
			return {
				filters: {
					type: "earning"
				}
			}
		})
		frm.set_query("salary_component", "deductions", function() {
			return {
				filters: {
					type: "deduction"
				}
			}
		})
	},

	start_date: function(frm){
		if(frm.doc.start_date){
			frm.trigger("set_end_date");
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
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	},

	company: function(frm) {
		var company = locals[':Company'][frm.doc.company];
		if(!frm.doc.letter_head && company.default_letter_head) {
			frm.set_value('letter_head', company.default_letter_head);
		}
	},

	refresh: function(frm) {
		frm.trigger("toggle_fields")
<<<<<<< HEAD
		frm.trigger("toggle_reqd_fields")
		var salary_detail_fields = ['formula', 'abbr', 'statistical_component']
		cur_frm.fields_dict['earnings'].grid.set_column_disp(salary_detail_fields,false);
		cur_frm.fields_dict['deductions'].grid.set_column_disp(salary_detail_fields,false);
	},	

	salary_slip_based_on_timesheet: function(frm) {
		frm.trigger("toggle_fields");
		frm.set_value('start_date', '');
	},
	
	payroll_frequency: function(frm) {
		frm.trigger("toggle_fields");
		frm.set_value('start_date', '');
	},

	employee: function(frm){
		frm.set_value('start_date', '');
	},

	toggle_fields: function(frm) {
		frm.toggle_display(['hourly_wages', 'timesheets'],
			cint(frm.doc.salary_slip_based_on_timesheet)==1);

		frm.toggle_display(['payment_days', 'total_working_days', 'leave_without_pay'],
			frm.doc.payroll_frequency!="");
	}
	
})

frappe.ui.form.on('Salary Detail', {
	earnings_remove: function(frm, dt, dn) {
		calculate_all(frm.doc, dt, dn);
	},
	deductions_remove: function(frm, dt, dn) {
		calculate_all(frm.doc, dt, dn);
	}
})

// Get leave details
//---------------------------------------------------------------------
cur_frm.cscript.start_date = function(doc, dt, dn){
	if(!doc.start_date){
		return frappe.call({
			method: 'get_emp_and_leave_details',
			doc: locals[dt][dn],
			callback: function(r, rt) {
				cur_frm.refresh();
				calculate_all(doc, dt, dn);
			}
		});
	}
}

cur_frm.cscript.payroll_frequency = cur_frm.cscript.salary_slip_based_on_timesheet = cur_frm.cscript.start_date;

cur_frm.cscript.employee = function(doc,dt,dn){
	doc.salary_structure = ''
	cur_frm.cscript.start_date(doc, dt, dn)
}

cur_frm.cscript.leave_without_pay = function(doc,dt,dn){
	if (doc.employee && doc.start_date && doc.end_date) {
=======
	},

	salary_slip_based_on_timesheet: function(frm) {
		frm.trigger("toggle_fields")
	},

	toggle_fields: function(frm) {
		frm.toggle_display(['start_date', 'end_date', 'hourly_wages', 'timesheets'],
			cint(frm.doc.salary_slip_based_on_timesheet)==1);
		frm.toggle_display(['fiscal_year', 'month', 'total_days_in_month', 'leave_without_pay', 'payment_days'],
			cint(frm.doc.salary_slip_based_on_timesheet)==0);
	}
})


frappe.ui.form.on("Salary Slip Timesheet", {
	time_sheet: function(frm, cdt, cdn) {
		doc = frm.doc;
		cur_frm.cscript.fiscal_year(doc, cdt, cdn)
	}
})


// On load
// -------------------------------------------------------------------
cur_frm.cscript.onload = function(doc,dt,dn){
	if((cint(doc.__islocal) == 1) && !doc.amended_from){
		if(!doc.month) {
			var today=new Date();
			month = (today.getMonth()+01).toString();
			if(month.length>1) doc.month = month;
			else doc.month = '0'+month;
		}
		if(!doc.fiscal_year) doc.fiscal_year = sys_defaults['fiscal_year'];
		refresh_many(['month', 'fiscal_year']);
	}
}

// Get leave details
//---------------------------------------------------------------------
cur_frm.cscript.fiscal_year = function(doc,dt,dn){
		return $c_obj(doc, 'get_emp_and_leave_details','',function(r, rt) {
			var doc = locals[dt][dn];
			cur_frm.refresh();
			calculate_all(doc, dt, dn);
		});
}

cur_frm.cscript.month = cur_frm.cscript.salary_slip_based_on_timesheet = cur_frm.cscript.fiscal_year;
cur_frm.cscript.start_date = cur_frm.cscript.end_date = cur_frm.cscript.fiscal_year;

cur_frm.cscript.employee = function(doc,dt,dn){
	doc.salary_structure = ''
	cur_frm.cscript.fiscal_year(doc, dt, dn)
}

cur_frm.cscript.leave_without_pay = function(doc,dt,dn){
	if (doc.employee && doc.fiscal_year && doc.month) {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		return $c_obj(doc, 'get_leave_details', {"lwp": doc.leave_without_pay}, function(r, rt) {
			var doc = locals[dt][dn];
			cur_frm.refresh();
			calculate_all(doc, dt, dn);
		});
	}
}

var calculate_all = function(doc, dt, dn) {
	calculate_earning_total(doc, dt, dn);
	calculate_ded_total(doc, dt, dn);
	calculate_net_pay(doc, dt, dn);
}

cur_frm.cscript.amount = function(doc,dt,dn){
<<<<<<< HEAD
	var child = locals[dt][dn];
	if(!doc.salary_structure){
		frappe.model.set_value(dt,dn, "default_amount", child.amount)
	}
	calculate_all(doc, dt, dn);
=======
	calculate_earning_total(doc, dt, dn);
	calculate_net_pay(doc, dt, dn);
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
}

cur_frm.cscript.depends_on_lwp = function(doc,dt,dn){
	calculate_earning_total(doc, dt, dn, true);
<<<<<<< HEAD
	calculate_ded_total(doc, dt, dn, true);
	calculate_net_pay(doc, dt, dn);
	refresh_many(['amount','gross_pay', 'rounded_total', 'net_pay', 'loan_repayment']);
=======
	calculate_net_pay(doc, dt, dn);
}
// Trigger on earning modified amount and depends on lwp
// ------------------------------------------------------------------------
cur_frm.cscript.amount = function(doc,dt,dn){
	calculate_ded_total(doc, dt, dn);
	calculate_net_pay(doc, dt, dn);
}

cur_frm.cscript.depends_on_lwp = function(doc, dt, dn) {
	calculate_ded_total(doc, dt, dn, true);
	calculate_net_pay(doc, dt, dn);
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
};

// Calculate earning total
// ------------------------------------------------------------------------
var calculate_earning_total = function(doc, dt, dn, reset_amount) {
	var tbl = doc.earnings || [];
	var total_earn = 0;
	for(var i = 0; i < tbl.length; i++){
		if(cint(tbl[i].depends_on_lwp) == 1) {
			tbl[i].amount =  Math.round(tbl[i].default_amount)*(flt(doc.payment_days) /
<<<<<<< HEAD
				cint(doc.total_working_days)*100)/100;
=======
				cint(doc.total_days_in_month)*100)/100;
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			refresh_field('amount', tbl[i].name, 'earnings');
		} else if(reset_amount) {
			tbl[i].amount = tbl[i].default_amount;
			refresh_field('amount', tbl[i].name, 'earnings');
		}
		total_earn += flt(tbl[i].amount);
<<<<<<< HEAD
	}
	doc.gross_pay = total_earn;
=======
		
	}
	doc.gross_pay = total_earn + flt(doc.arrear_amount) + flt(doc.leave_encashment_amount);
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	refresh_many(['amount','gross_pay']);
}

// Calculate deduction total
// ------------------------------------------------------------------------
var calculate_ded_total = function(doc, dt, dn, reset_amount) {
	var tbl = doc.deductions || [];
	var total_ded = 0;
	for(var i = 0; i < tbl.length; i++){
		if(cint(tbl[i].depends_on_lwp) == 1) {
<<<<<<< HEAD
			tbl[i].amount = Math.round(tbl[i].default_amount)*(flt(doc.payment_days)/cint(doc.total_working_days)*100)/100;
=======
			tbl[i].amount = Math.round(tbl[i].default_amount)*(flt(doc.payment_days)/cint(doc.total_days_in_month)*100)/100;
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			refresh_field('amount', tbl[i].name, 'deductions');
		} else if(reset_amount) {
			tbl[i].amount = tbl[i].default_amount;
			refresh_field('amount', tbl[i].name, 'deductions');
		}
		total_ded += flt(tbl[i].amount);
	}
	doc.total_deduction = total_ded;
	refresh_field('total_deduction');
}

// Calculate net payable amount
// ------------------------------------------------------------------------
var calculate_net_pay = function(doc, dt, dn) {
	doc.net_pay = flt(doc.gross_pay) - flt(doc.total_deduction);
	doc.rounded_total = Math.round(doc.net_pay);
	refresh_many(['net_pay', 'rounded_total']);
}

<<<<<<< HEAD
=======
// trigger on arrear
// ------------------------------------------------------------------------
cur_frm.cscript.arrear_amount = function(doc,dt,dn){
	calculate_earning_total(doc, dt, dn);
	calculate_net_pay(doc, dt, dn);
}

// trigger on encashed amount
// ------------------------------------------------------------------------
cur_frm.cscript.leave_encashment_amount = cur_frm.cscript.arrear_amount;

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
// validate
// ------------------------------------------------------------------------
cur_frm.cscript.validate = function(doc, dt, dn) {
	calculate_all(doc, dt, dn);
}

cur_frm.fields_dict.employee.get_query = function(doc,cdt,cdn) {
	return{
		query: "erpnext.controllers.queries.employee_query"
	}
}
