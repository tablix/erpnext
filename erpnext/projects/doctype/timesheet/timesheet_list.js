frappe.listview_settings['Timesheet'] = {
<<<<<<< HEAD
	add_fields: ["status", "total_hours", "start_date", "end_date"],
=======
	add_fields: ["employee_name", "start_date"],
	onload: function(listview) {
		frappe.route_options = {
			"owner": user
			};
		},
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
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