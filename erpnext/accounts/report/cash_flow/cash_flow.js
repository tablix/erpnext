// Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.require("assets/erpnext/js/financial_statements.js", function() {
<<<<<<< HEAD
	frappe.query_reports["Cash Flow"] = $.extend({},
		erpnext.financial_statements);
=======
	frappe.query_reports["Cash Flow"] = erpnext.financial_statements;
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	frappe.query_reports["Cash Flow"]["filters"].push({
		"fieldname": "accumulated_values",
		"label": __("Accumulated Values"),
		"fieldtype": "Check"
	});
});