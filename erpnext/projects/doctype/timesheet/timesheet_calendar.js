frappe.views.calendar["Timesheet"] = {
	field_map: {
<<<<<<< HEAD
		"start": "start_date",
		"end": "end_date",
		"name": "parent",
		"id": "name",
		"allDay": "allDay",
		"child_name": "name",
		"title": "title"
	},
	style_map: {
		"0": "info", 
		"1": "standard", 
		"2": "danger"
=======
		"start": "from_time",
		"end": "to_time",
		"name": "parent",
		"id": "parent",
		"title": "activity_type",
		"allDay": "allDay",
		"child_name": "name"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	},
	gantt: true,
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "project",
			"options": "Project",
			"label": __("Project")
		},
		{
			"fieldtype": "Link",
			"fieldname": "employee",
			"options": "Employee",
			"label": __("Employee")
		}
	],
	get_events_method: "erpnext.projects.doctype.timesheet.timesheet.get_events"
<<<<<<< HEAD
}
=======
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
