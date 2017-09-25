frappe.listview_settings['Attendance'] = {
<<<<<<< HEAD
	add_fields: ["status", "attendance_date"],
=======
	add_fields: ["status", "att_date"],
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	get_indicator: function(doc) {
		return [__(doc.status), doc.status=="Present" ? "green" : "darkgrey", "status,=," + doc.status];
	}
};
