// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["WPS SIF Report"] = {
	"filters": [
		{
			"fieldname":"month",
			"label": __("Month"),
			"fieldtype": "Int",
			"default": 1
		},
		{
			"fieldname":"year",
			"label": __("Year"),
			"fieldtype": "Int",
			"default": 2017
		}
	]
}
