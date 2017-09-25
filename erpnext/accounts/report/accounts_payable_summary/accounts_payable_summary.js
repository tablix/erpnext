// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Accounts Payable Summary"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname":"supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier"
		},
		{
			"fieldname":"report_date",
			"label": __("Date"),
			"fieldtype": "Date",
<<<<<<< HEAD
			"default": frappe.datetime.get_today()
=======
			"default": get_today()
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		},
		{
			"fieldname":"ageing_based_on",
			"label": __("Ageing Based On"),
			"fieldtype": "Select",
<<<<<<< HEAD
			"options": 'Posting Date\nDue Date',
=======
			"options": 'Posting Date' + NEWLINE + 'Due Date',
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			"default": "Posting Date"
		},
		{
			"fieldtype": "Break",
		},
		{
			"fieldname":"range1",
			"label": __("Ageing Range 1"),
			"fieldtype": "Int",
			"default": "30",
			"reqd": 1
		},
		{
			"fieldname":"range2",
			"label": __("Ageing Range 2"),
			"fieldtype": "Int",
			"default": "60",
			"reqd": 1
		},
		{
			"fieldname":"range3",
			"label": __("Ageing Range 3"),
			"fieldtype": "Int",
			"default": "90",
			"reqd": 1
		}
<<<<<<< HEAD
	],

	onload: function(report) {
		report.page.add_inner_button(__("Accounts Payable"), function() {
			var filters = report.get_values();
			frappe.set_route('query-report', 'Accounts Payable', {company: filters.company});
		});
	}
=======
	]
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
}
