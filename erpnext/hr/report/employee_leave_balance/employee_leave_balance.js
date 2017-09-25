// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Employee Leave Balance"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
<<<<<<< HEAD
			"default": frappe.defaults.get_default("year_start_date")
=======
			"default": frappe.datetime.year_start()
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
<<<<<<< HEAD
			"default": frappe.defaults.get_default("year_end_date")
=======
			"default": frappe.datetime.year_end()
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": frappe.defaults.get_user_default("Company")
		}
	]
<<<<<<< HEAD
}
=======
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
