// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

cur_frm.add_fetch('employee', 'company', 'company');
cur_frm.add_fetch('employee', 'employee_name', 'employee_name');

cur_frm.cscript.onload = function(doc, cdt, cdn) {
<<<<<<< HEAD
	if(doc.__islocal) cur_frm.set_value("attendance_date", frappe.datetime.get_today());
=======
	if(doc.__islocal) cur_frm.set_value("att_date", get_today());
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
}

cur_frm.fields_dict.employee.get_query = function(doc,cdt,cdn) {
	return{
		query: "erpnext.controllers.queries.employee_query"
	}	
}
