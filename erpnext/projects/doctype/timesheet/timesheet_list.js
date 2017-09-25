frappe.listview_settings['Timesheet'] = {
	add_fields: ["employee_name", "start_date"],
	onload: function(listview) {
		frappe.route_options = {
			"owner": user
			};
		},
	get_indicator: function(doc) {
		if (doc.status== "Billed") {
			return [__("Billed"), "green", "status,=," + "Billed"]
		}
		
		if (doc.status== "Payslip") {
			return [__("Payslip"), "green", "status,=," + "Payslip"]
		}
		
		if (doc.status== "Completed") {
			return [__("Completed"), "green", "status,=," + "Completed"]
		}
	}
};