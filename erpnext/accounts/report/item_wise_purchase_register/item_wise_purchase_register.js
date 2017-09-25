// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Item-wise Purchase Register"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
<<<<<<< HEAD
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
=======
			"default": frappe.defaults.get_user_default("year_start_date"),
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
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
			"fieldname": "item_code",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item",
		},
		{
			"fieldname":"supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier"
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname":"mode_of_payment",
			"label": __("Mode of Payment"),
			"fieldtype": "Link",
			"options": "Mode of Payment"
		}
	]
}
