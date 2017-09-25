from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
<<<<<<< HEAD
			"label": _("Issues"),
=======
			"label": _("Maintance"),
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			"items": [
				{
					"type": "doctype",
					"name": "Issue",
					"description": _("Support queries from customers."),
<<<<<<< HEAD
=======
					"label":"Case"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				},
				{
					"type": "doctype",
					"name": "Communication",
					"description": _("Communication log."),
				},
<<<<<<< HEAD
=======
				
				{
					"type": "doctype",
					"name": "Maintenance Contract",
					"description": _("Maintenance Contract for Support")
				},
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			]
		},
		{
			"label": _("Warranty"),
			"items": [
				{
					"type": "doctype",
					"name": "Warranty Claim",
					"description": _("Warranty Claim against Serial No."),
				},
				{
					"type": "doctype",
					"name": "Serial No",
					"description": _("Single unit of an Item."),
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
					"type": "page",
					"name": "support-analytics",
					"label": _("Support Analytics"),
<<<<<<< HEAD
					"icon": "fa fa-bar-chart"
=======
					"icon": "icon-bar-chart"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				},
				{
					"type": "report",
					"name": "Minutes to First Response for Issues",
					"doctype": "Issue",
					"is_query_report": True
				},
<<<<<<< HEAD
				{
					"type": "report",
					"name": "Support Hours",
					"doctype": "Issue",
					"is_query_report": True
				},
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			]
		},
	]
