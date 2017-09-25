from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Maintance"),
			"items": [
				{
					"type": "doctype",
					"name": "Issue",
					"description": _("Support queries from customers."),
					"label":"Case"
				},
				{
					"type": "doctype",
					"name": "Communication",
					"description": _("Communication log."),
				},
				
				{
					"type": "doctype",
					"name": "Maintenance Contract",
					"description": _("Maintenance Contract for Support")
				},
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
			"icon": "icon-list",
			"items": [
				{
					"type": "page",
					"name": "support-analytics",
					"label": _("Support Analytics"),
					"icon": "icon-bar-chart"
				},
				{
					"type": "report",
					"name": "Minutes to First Response for Issues",
					"doctype": "Issue",
					"is_query_report": True
				},
			]
		},
	]
