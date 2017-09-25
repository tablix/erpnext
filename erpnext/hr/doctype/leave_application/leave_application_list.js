frappe.listview_settings['Leave Application'] = {
<<<<<<< HEAD
	add_fields: ["status", "leave_type", "employee", "employee_name", "total_leave_days", "from_date", "to_date"],
=======
	add_fields: ["status", "leave_type", "employee", "employee_name", "total_leave_days", "from_date"],
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	filters:[["status","!=", "Rejected"]],
	get_indicator: function(doc) {
		return [__(doc.status), frappe.utils.guess_colour(doc.status),
			"status,=," + doc.status];
	}
};
