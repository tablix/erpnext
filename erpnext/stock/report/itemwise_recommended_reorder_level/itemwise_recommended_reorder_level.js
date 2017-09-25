// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Itemwise Recommended Reorder Level"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
<<<<<<< HEAD
			"default": frappe.sys_defaults.year_start_date
=======
			"default": sys_defaults.year_start_date
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
<<<<<<< HEAD
			"default": frappe.datetime.get_today()
=======
			"default": get_today()
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		}
	]
}