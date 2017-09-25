// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Bank Reconciliation Statement"] = {
	"filters": [
		{
			"fieldname":"account",
			"label": __("Bank Account"),
			"fieldtype": "Link",
			"options": "Account",
<<<<<<< HEAD
			"default": frappe.defaults.get_user_default("Company")? 
				locals[":Company"][frappe.defaults.get_user_default("Company")]["default_bank_account"]: "",
=======
			"default": locals[":Company"][frappe.defaults.get_user_default("Company")]["default_bank_account"],
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			"reqd": 1,
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
		{
			"fieldname":"report_date",
			"label": __("Date"),
			"fieldtype": "Date",
<<<<<<< HEAD
			"default": frappe.datetime.get_today(),
=======
			"default": get_today(),
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			"reqd": 1
		},
	]
}
