frappe.listview_settings['Project'] = {
<<<<<<< HEAD
	add_fields: ["status", "priority", "is_active", "percent_complete", "expected_end_date", "project_name"],
=======
	add_fields: ["status", "priority", "is_active", "percent_complete", "expected_end_date"],
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	filters:[["status","=", "Open"]],
	get_indicator: function(doc) {
		if(doc.status=="Open" && doc.percent_complete) {
			return [__("{0}% Complete", [cint(doc.percent_complete)]), "orange", "percent_complete,>,0|status,=,Open"];
		} else {
			return [__(doc.status), frappe.utils.guess_colour(doc.status), "status,=," + doc.status];
		}
	}
};
