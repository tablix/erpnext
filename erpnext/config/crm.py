from frappe import _

def get_data():
	return [
		{
			"label": _("Sales Pipeline"),
<<<<<<< HEAD
			"icon": "fa fa-star",
=======
			"icon": "icon-star",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			"items": [
				{
					"type": "doctype",
					"name": "Lead",
					"description": _("Database of potential customers."),
				},
				{
					"type": "doctype",
					"name": "Opportunity",
					"description": _("Potential opportunities for selling."),
				},
				{
					"type": "doctype",
					"name": "Customer",
					"description": _("Customer database."),
				},
				{
					"type": "doctype",
					"name": "Contact",
					"description": _("All Contacts."),
				},
			]
		},
		{
			"label": _("Reports"),
<<<<<<< HEAD
			"icon": "fa fa-list",
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Lead Details",
					"doctype": "Lead"
				},
				{
					"type": "page",
					"name": "sales-funnel",
					"label": _("Sales Funnel"),
					"icon": "fa fa-bar-chart",
				},
				{
					"type": "report",
					"name": "Prospects Engaged But Not Converted",
					"doctype": "Lead",
					"is_query_report": True
=======
			"icon": "icon-list",
			"items": [
				{
					"type": "page",
					"name": "sales-funnel",
					"label": _("Sales Funnel"),
					"icon": "icon-bar-chart",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				},
				{
					"type": "report",
					"name": "Minutes to First Response for Opportunity",
					"doctype": "Opportunity",
					"is_query_report": True
				},
				{
					"type": "report",
					"is_query_report": True,
<<<<<<< HEAD
					"name": "Customer Addresses And Contacts",
					"doctype": "Contact"
=======
					"name": "Lead Details",
					"doctype": "Lead"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				},
				{
					"type": "report",
					"is_query_report": True,
<<<<<<< HEAD
					"name": "Inactive Customers",
					"doctype": "Sales Order"
=======
					"name": "Customer Addresses and Contacts",
					"doctype": "Contact"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				},
				{
					"type": "report",
					"is_query_report": True,
<<<<<<< HEAD
					"name": "Campaign Efficiency",
					"doctype": "Lead"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Lead Owner Efficiency",
					"doctype": "Lead"
				}
=======
					"name": "Inactive Customers",
					"doctype": "Sales Order"
				},
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			]
		},
		{
			"label": _("Communication"),
<<<<<<< HEAD
			"icon": "fa fa-star",
=======
			"icon": "icon-star",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			"items": [
				{
					"type": "doctype",
					"name": "Communication",
					"description": _("Record of all communications of type email, phone, chat, visit, etc."),
				},
			]
		},
		{
			"label": _("Setup"),
<<<<<<< HEAD
			"icon": "fa fa-cog",
=======
			"icon": "icon-cog",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			"items": [
				{
					"type": "doctype",
					"name": "Campaign",
					"description": _("Sales campaigns."),
				},
				{
					"type": "doctype",
					"label": _("Customer Group"),
					"name": "Customer Group",
<<<<<<< HEAD
					"icon": "fa fa-sitemap",
=======
					"icon": "icon-sitemap",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
					"link": "Tree/Customer Group",
					"description": _("Manage Customer Group Tree."),
				},
				{
					"type": "doctype",
					"label": _("Territory"),
					"name": "Territory",
<<<<<<< HEAD
					"icon": "fa fa-sitemap",
=======
					"icon": "icon-sitemap",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
					"link": "Tree/Territory",
					"description": _("Manage Territory Tree."),
				},
				{
					"type": "doctype",
					"label": _("Sales Person"),
					"name": "Sales Person",
<<<<<<< HEAD
					"icon": "fa fa-sitemap",
=======
					"icon": "icon-sitemap",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
					"link": "Tree/Sales Person",
					"description": _("Manage Sales Person Tree."),
				},
			]
		},
		{
			"label": _("SMS"),
<<<<<<< HEAD
			"icon": "fa fa-wrench",
=======
			"icon": "icon-wrench",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			"items": [
				{
					"type": "doctype",
					"name": "SMS Center",
					"description":_("Send mass SMS to your contacts"),
				},
				{
					"type": "doctype",
					"name": "SMS Log",
					"description":_("Logs for maintaining sms delivery status"),
				},
				{
					"type": "doctype",
					"name": "SMS Settings",
					"description": _("Setup SMS gateway settings")
				}
			]
		},
		{
			"label": _("Help"),
			"items": [
				{
					"type": "help",
					"label": _("Lead to Quotation"),
					"youtube_id": "TxYX4r4JAKA"
				},
				{
					"type": "help",
					"label": _("Newsletters"),
					"youtube_id": "muLKsCrrDRo"
				},
			]
		},
	]
