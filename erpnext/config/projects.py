from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Projects"),
<<<<<<< HEAD
			"icon": "fa fa-star",
=======
			"icon": "icon-star",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			"items": [
				{
					"type": "doctype",
					"name": "Project",
					"description": _("Project master."),
				},
				{
					"type": "doctype",
					"name": "Task",
					"description": _("Project activity / task."),
				},
				{
<<<<<<< HEAD
					"type": "doctype",
					"name": "Project Type",
					"description": _("Define Project type."),
				},
				{
					"type": "report",
					"route": "List/Task/Gantt",
=======
					"type": "report",
					"route": "Gantt/Task",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
					"doctype": "Task",
					"name": "Gantt Chart",
					"description": _("Gantt chart of all tasks.")
				},
			]
		},
		{
			"label": _("Time Tracking"),
			"items": [
				{
					"type": "doctype",
					"name": "Timesheet",
					"description": _("Timesheet for tasks."),
				},
				{
					"type": "doctype",
					"name": "Activity Type",
					"description": _("Types of activities for Time Logs"),
				},
				{
					"type": "doctype",
					"name": "Activity Cost",
					"description": _("Cost of various activities"),
				},
			]
		},
		{
			"label": _("Reports"),
<<<<<<< HEAD
			"icon": "fa fa-list",
=======
			"icon": "icon-list",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Daily Timesheet Summary",
					"doctype": "Timesheet"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Project wise Stock Tracking",
					"doctype": "Project"
				},
			]
		},
		{
			"label": _("Help"),
<<<<<<< HEAD
			"icon": "fa fa-facetime-video",
=======
			"icon": "icon-facetime-video",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			"items": [
				{
					"type": "help",
					"label": _("Managing Projects"),
					"youtube_id": "egxIGwtoKI4"
				},
			]
		},
	]
