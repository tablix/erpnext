// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.views.calendar["Task"] = {
	field_map: {
		"start": "exp_start_date",
		"end": "exp_end_date",
		"id": "name",
		"title": "subject",
<<<<<<< HEAD
		"allDay": "allDay",
		"progress": "progress"
=======
		"allDay": "allDay"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	},
	gantt: true,
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "project",
			"options": "Project",
			"label": __("Project")
		}
	],
	get_events_method: "erpnext.projects.doctype.task.task.get_events"
}
