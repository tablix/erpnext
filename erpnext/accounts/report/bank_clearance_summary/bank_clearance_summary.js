// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Bank Clearance Summary"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_user_default("year_start_date"),
			"width": "80"
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
		},
		{
			"fieldname":"account",
			"label": __("Bank Account"),
			"fieldtype": "Link",
			"options": "Account",
			"reqd": 1,
<<<<<<< HEAD
			"default": frappe.defaults.get_user_default("Company")? 
				locals[":Company"][frappe.defaults.get_user_default("Company")]["default_bank_account"]: "",
=======
			"default": locals[":Company"][frappe.defaults.get_user_default("Company")]["default_bank_account"],
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			"get_query": function() {
				return {
					"query": "erpnext.controllers.queries.get_account_list",
					"filters": [
						['Account', 'account_type', 'in', 'Bank, Cash'],
						['Account', 'is_group', '=', 0],
					]
				}
			}
		},
	]
}
