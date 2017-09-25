from __future__ import unicode_literals
from frappe import _
<<<<<<< HEAD
=======
from . import __version__ as app_version
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

app_name = "erpnext"
app_title = "ERPNext"
app_publisher = "Frappe Technologies Pvt. Ltd."
app_description = """ERP made simple"""
<<<<<<< HEAD
app_icon = "fa fa-th"
=======
app_icon = "icon-th"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
app_color = "#e74c3c"
app_email = "info@erpnext.com"
app_license = "GNU General Public License (v3)"
source_link = "https://github.com/frappe/erpnext"

<<<<<<< HEAD
develop_version = '8.x.x-beta'

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
error_report_email = "support@erpnext.com"

app_include_js = "assets/js/erpnext.min.js"
app_include_css = "assets/css/erpnext.css"
web_include_js = "assets/js/erpnext-web.min.js"
web_include_css = "assets/erpnext/css/website.css"

<<<<<<< HEAD
doctype_js = {
	"Communication": "public/js/communication.js",
}

# setup wizard
setup_wizard_requires = "assets/erpnext/js/setup_wizard.js"
setup_wizard_complete = "erpnext.setup.setup_wizard.setup_wizard.setup_complete"
setup_wizard_success = "erpnext.setup.setup_wizard.setup_wizard.setup_success"
setup_wizard_test = "erpnext.setup.setup_wizard.test_setup_wizard.run_setup_wizard_test"
=======
# setup wizard
setup_wizard_requires = "assets/erpnext/js/setup_wizard.js"
setup_wizard_complete = "erpnext.setup.setup_wizard.setup_wizard.setup_complete"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

before_install = "erpnext.setup.install.check_setup_wizard_not_completed"
after_install = "erpnext.setup.install.after_install"

boot_session = "erpnext.startup.boot.boot_session"
notification_config = "erpnext.startup.notifications.get_notification_config"
<<<<<<< HEAD
get_help_messages = "erpnext.utilities.activation.get_help_messages"
get_user_progress_slides = "erpnext.utilities.user_progress.get_user_progress_slides"
update_and_get_user_progress = "erpnext.utilities.user_progress_utils.update_default_domain_actions_and_get_state"
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

on_session_creation = "erpnext.shopping_cart.utils.set_cart_count"
on_logout = "erpnext.shopping_cart.utils.clear_cart_count"

<<<<<<< HEAD
treeviews = ['Account', 'Cost Center', 'Warehouse', 'Item Group', 'Customer Group', 'Sales Person', 'Territory']
=======
remember_selected = ['Company', 'Cost Center', 'Project']
treeviews = ['Account', 'Cost Center', 'Warehouse', 'Item Group', 'Customer Group', 'Sales Person', 'Territory', "BOM"]
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

# website
update_website_context = "erpnext.shopping_cart.utils.update_website_context"
my_account_context = "erpnext.shopping_cart.utils.update_my_account_context"

email_append_to = ["Job Applicant", "Opportunity", "Issue"]

calendars = ["Task", "Production Order", "Leave Application", "Sales Order", "Holiday List"]

fixtures = ["Web Form"]

<<<<<<< HEAD
website_generators = ["Item Group", "Item", "BOM", "Sales Partner",
	"Job Opening", "Student Admission"]

website_context = {
	"favicon": 	"/assets/erpnext/images/favicon.png",
	"splash_image": "/assets/erpnext/images/erp-icon.svg"
=======
website_generators = ["Item Group", "Item", "Sales Partner", "Job Opening"]

website_context = {
	"favicon": 	"/assets/erpnext/images/favicon.png",
	"splash_image": "/assets/erpnext/images/splash.png"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
}

website_route_rules = [
	{"from_route": "/orders", "to_route": "Sales Order"},
	{"from_route": "/orders/<path:name>", "to_route": "order",
		"defaults": {
			"doctype": "Sales Order",
<<<<<<< HEAD
			"parents": [{"label": _("Orders"), "route": "orders"}]
=======
			"parents": [{"title": _("Orders"), "name": "orders"}]
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		}
	},
	{"from_route": "/invoices", "to_route": "Sales Invoice"},
	{"from_route": "/invoices/<path:name>", "to_route": "order",
		"defaults": {
			"doctype": "Sales Invoice",
<<<<<<< HEAD
			"parents": [{"label": _("Invoices"), "route": "invoices"}]
		}
	},
	{"from_route": "/supplier-quotations", "to_route": "Supplier Quotation"},
	{"from_route": "/supplier-quotations/<path:name>", "to_route": "order",
		"defaults": {
			"doctype": "Supplier Quotation",
			"parents": [{"label": _("Supplier Quotation"), "route": "quotations"}]
		}
	},
	{"from_route": "/quotations", "to_route": "Quotation"},
	{"from_route": "/quotations/<path:name>", "to_route": "order",
		"defaults": {
			"doctype": "Quotation",
			"parents": [{"label": _("Quotations"), "route": "quotations"}]
=======
			"parents": [{"title": _("Invoices"), "name": "invoices"}]
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		}
	},
	{"from_route": "/shipments", "to_route": "Delivery Note"},
	{"from_route": "/shipments/<path:name>", "to_route": "order",
		"defaults": {
			"doctype": "Delivery Note",
<<<<<<< HEAD
			"parents": [{"label": _("Shipments"), "route": "shipments"}]
=======
			"parents": [{"title": _("Shipments"), "name": "shipments"}]
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		}
	},
	{"from_route": "/rfq", "to_route": "Request for Quotation"},
	{"from_route": "/rfq/<path:name>", "to_route": "rfq",
		"defaults": {
			"doctype": "Request for Quotation",
<<<<<<< HEAD
			"parents": [{"label": _("Request for Quotation"), "route": "rfq"}]
=======
			"parents": [{"title": _("Request for Quotation"), "name": "rfq"}]
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		}
	},
	{"from_route": "/addresses", "to_route": "Address"},
	{"from_route": "/addresses/<path:name>", "to_route": "addresses",
		"defaults": {
			"doctype": "Address",
<<<<<<< HEAD
			"parents": [{"label": _("Addresses"), "route": "addresses"}]
		}
	},
	{"from_route": "/jobs", "to_route": "Job Opening"},
	{"from_route": "/admissions", "to_route": "Student Admission"},
	{"from_route": "/boms", "to_route": "BOM"},
	{"from_route": "/timesheets", "to_route": "Timesheet"},
]

standard_portal_menu_items = [
	{"title": _("Projects"), "route": "/project", "reference_doctype": "Project"},
	{"title": _("Request for Quotations"), "route": "/rfq", "reference_doctype": "Request for Quotation", "role": "Supplier"},
	{"title": _("Supplier Quotation"), "route": "/supplier-quotations", "reference_doctype": "Supplier Quotation", "role": "Supplier"},
	{"title": _("Quotations"), "route": "/quotations", "reference_doctype": "Quotation", "role":"Customer"},
	{"title": _("Orders"), "route": "/orders", "reference_doctype": "Sales Order", "role":"Customer"},
	{"title": _("Invoices"), "route": "/invoices", "reference_doctype": "Sales Invoice", "role":"Customer"},
	{"title": _("Shipments"), "route": "/shipments", "reference_doctype": "Delivery Note", "role":"Customer"},
	{"title": _("Issues"), "route": "/issues", "reference_doctype": "Issue", "role":"Customer"},
	{"title": _("Addresses"), "route": "/addresses", "reference_doctype": "Address"},
	{"title": _("Timesheets"), "route": "/timesheets", "reference_doctype": "Timesheet", "role":"Customer"},
	{"title": _("Timesheets"), "route": "/timesheets", "reference_doctype": "Timesheet", "role":"Customer"},
	{"title": _("Lab Test"), "route": "/lab-test", "reference_doctype": "Lab Test", "role":"Patient"},
	{"title": _("Prescription"), "route": "/prescription", "reference_doctype": "Consultation", "role":"Patient"},
	{"title": _("Patient Appointment"), "route": "/patient-appointments", "reference_doctype": "Patient Appointment", "role":"Patient"},
	{"title": _("Fees"), "route": "/fees", "reference_doctype": "Fees", "role":"Student"},
	{"title": _("Newsletter"), "route": "/newsletters", "reference_doctype": "Newsletter"}
]

default_roles = [
	{'role': 'Customer', 'doctype':'Contact', 'email_field': 'email_id'},
	{'role': 'Supplier', 'doctype':'Contact', 'email_field': 'email_id'},
	{'role': 'Student', 'doctype':'Student', 'email_field': 'student_email_id'},
=======
			"parents": [{"title": _("Addresses"), "name": "addresses"}]
		}
	},
	{"from_route": "/jobs", "to_route": "Job Opening"},
]

portal_menu_items = [
	{"title": _("Projects"), "route": "/project", "reference_doctype": "Project"},
	{"title": _("Request for Quotations"), "route": "/rfq", "reference_doctype": "Request for Quotation"},
	{"title": _("Orders"), "route": "/orders", "reference_doctype": "Sales Order"},
	{"title": _("Invoices"), "route": "/invoices", "reference_doctype": "Sales Invoice"},
	{"title": _("Shipments"), "route": "/shipments", "reference_doctype": "Delivery Note"},
	{"title": _("Issues"), "route": "/issues", "reference_doctype": "Issue", "show_always": True},
	{"title": _("Addresses"), "route": "/addresses", "reference_doctype": "Address"},
	{"title": _("Announcements"), "route": "/announcement", "reference_doctype": "Announcement"},
	{"title": _("Courses"), "route": "/course", "reference_doctype": "Course"},
	{"title": _("Assessment Schedule"), "route": "/assessment", "reference_doctype": "Assessment"},
	{"title": _("Fees"), "route": "/fees", "reference_doctype": "Fees"}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
]

has_website_permission = {
	"Sales Order": "erpnext.controllers.website_list_for_contact.has_website_permission",
<<<<<<< HEAD
	"Quotation": "erpnext.controllers.website_list_for_contact.has_website_permission",
	"Sales Invoice": "erpnext.controllers.website_list_for_contact.has_website_permission",
	"Supplier Quotation": "erpnext.controllers.website_list_for_contact.has_website_permission",
	"Delivery Note": "erpnext.controllers.website_list_for_contact.has_website_permission",
	"Issue": "erpnext.support.doctype.issue.issue.has_website_permission",
	"Timesheet": "erpnext.controllers.website_list_for_contact.has_website_permission",
	"Lab Test": "erpnext.healthcare.web_form.lab_test.lab_test.has_website_permission",
	"Consultation": "erpnext.healthcare.web_form.prescription.prescription.has_website_permission",
	"Patient Appointment": "erpnext.healthcare.web_form.patient_appointments.patient_appointments.has_website_permission"
=======
	"Sales Invoice": "erpnext.controllers.website_list_for_contact.has_website_permission",
	"Delivery Note": "erpnext.controllers.website_list_for_contact.has_website_permission",
	"Issue": "erpnext.support.doctype.issue.issue.has_website_permission",
	"Address": "erpnext.utilities.doctype.address.address.has_website_permission",
	"Discussion": "erpnext.schools.web_form.discussion.discussion.has_website_permission"
}

permission_query_conditions = {
	"Contact": "erpnext.utilities.address_and_contact.get_permission_query_conditions_for_contact",
	"Address": "erpnext.utilities.address_and_contact.get_permission_query_conditions_for_address"
}

has_permission = {
	"Contact": "erpnext.utilities.address_and_contact.has_permission",
	"Address": "erpnext.utilities.address_and_contact.has_permission"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
}

dump_report_map = "erpnext.startup.report_data_map.data_map"

before_tests = "erpnext.setup.utils.before_tests"

standard_queries = {
	"Customer": "erpnext.selling.doctype.customer.customer.get_customer_list"
}

doc_events = {
	"Stock Entry": {
		"on_submit": "erpnext.stock.doctype.material_request.material_request.update_completed_and_requested_qty",
		"on_cancel": "erpnext.stock.doctype.material_request.material_request.update_completed_and_requested_qty"
	},
	"User": {
<<<<<<< HEAD
		"after_insert": "frappe.contacts.doctype.contact.contact.update_contact",
		"validate": "erpnext.hr.doctype.employee.employee.validate_employee_role",
		"on_update": ["erpnext.hr.doctype.employee.employee.update_user_permissions",
			"erpnext.portal.utils.set_default_role"]
=======
		"validate": "erpnext.hr.doctype.employee.employee.validate_employee_role",
		"on_update": "erpnext.hr.doctype.employee.employee.update_user_permissions",
		"on_update": "erpnext.utilities.doctype.contact.contact.update_contact"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	},
	("Sales Taxes and Charges Template", 'Price List'): {
		"on_update": "erpnext.shopping_cart.doctype.shopping_cart_settings.shopping_cart_settings.validate_cart_settings"
	},
<<<<<<< HEAD
=======
	"Address": {
		"validate": "erpnext.shopping_cart.cart.set_customer_in_address"
	},

	# bubble transaction notification on master
	('Opportunity', 'Quotation', 'Sales Order', 'Delivery Note', 'Sales Invoice',
		'Supplier Quotation', 'Purchase Order', 'Purchase Receipt',
		'Purchase Invoice', 'Project', 'Issue'): {
			'on_change': 'erpnext.accounts.party_status.notify_status'
		},
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	"Website Settings": {
		"validate": "erpnext.portal.doctype.products_settings.products_settings.home_page_is_products"
	},
	"Payment Entry": {
		"on_submit": "erpnext.accounts.doctype.payment_request.payment_request.make_status_as_paid"
<<<<<<< HEAD
	},
	'Address': {
		'validate': 'erpnext.regional.india.utils.validate_gstin_for_india'
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	}
}

scheduler_events = {
	"hourly": [
<<<<<<< HEAD
		"erpnext.accounts.doctype.subscription.subscription.make_subscription_entry",
		'erpnext.hr.doctype.daily_work_summary_settings.daily_work_summary_settings.trigger_emails'
=======
		"erpnext.controllers.recurring_document.create_recurring_documents"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	],
	"daily": [
		"erpnext.stock.reorder_item.reorder_item",
		"erpnext.setup.doctype.email_digest.email_digest.send",
		"erpnext.support.doctype.issue.issue.auto_close_tickets",
<<<<<<< HEAD
		"erpnext.crm.doctype.opportunity.opportunity.auto_close_opportunity",
		"erpnext.controllers.accounts_controller.update_invoice_status",
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		"erpnext.accounts.doctype.fiscal_year.fiscal_year.auto_create_fiscal_year",
		"erpnext.hr.doctype.employee.employee.send_birthday_reminders",
		"erpnext.projects.doctype.task.task.set_tasks_as_overdue",
		"erpnext.accounts.doctype.asset.depreciation.post_depreciation_entries",
<<<<<<< HEAD
		"erpnext.hr.doctype.daily_work_summary_settings.daily_work_summary_settings.send_summary",
		"erpnext.stock.doctype.serial_no.serial_no.update_maintenance_status",
		"erpnext.buying.doctype.supplier_scorecard.supplier_scorecard.refresh_scorecards",
		"erpnext.setup.doctype.company.company.cache_companies_monthly_sales_history",
		"erpnext.manufacturing.doctype.bom_update_tool.bom_update_tool.update_latest_price_in_all_boms",
	]
}

email_brand_image = "assets/erpnext/images/erpnext-logo.jpg"

default_mail_footer = """
	<span>
		Sent via
		<a class="text-muted" href="https://erpnext.com?source=via_email_footer" target="_blank">
			ERPNext
		</a>
	</span>
"""
=======
		"erpnext.hr.doctype.employee.employee.exp_doc",
		"erpnext.hr.doctype.opportunity.opportunity.rfqtime",
		"erpnext.hr.doctype.opportunity.opportunity.kam_time",
		"erpnext.hr.doctype.boq.boq.costing_time",
		"erpnext.hr.doctype.boq.boq.bdm_time",
		"erpnext.hr.doctype.boq.boq.kam_time",
		"erpnext.hr.doctype.boq.boq.cbdo_time",
		"erpnext.hr.doctype.sales_order.sales_order.kam_time",
		"erpnext.hr.doctype.sales_order.sales_order.cbdo_time",
		"erpnext.hr.doctype.sales_order.sales_order.cfo_time"
	],
	
	"monthly": [
		#"erpnext.hr.doctype.employee.employee.send_passport_expiry_reminders",
		#"erpnext.hr.doctype.employee.employee.send_labour_card_expiry_reminders",
		#"erpnext.hr.doctype.employee.employee.send_e_id_expiry_reminders",
		#"erpnext.hr.doctype.employee.employee.send_visa_expiry_reminders",
		#"erpnext.hr.doctype.employee.employee.send_health_card_reminders",
		#"erpnext.hr.doctype.employee.employee.send_vehicle_insurance_expiry_reminders",
		#"erpnext.hr.doctype.employee.employee.exp_doc"
		
	]
}

default_mail_footer = """<div style="text-align: center;">
	<a href="https://erpnext.com?source=via_email_footer" target="_blank" style="color: #8d99a6;">
		Sent via ERPNext
	</a>
</div>"""
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

get_translated_dict = {
	("doctype", "Global Defaults"): "frappe.geo.country_info.get_translated_dict"
}

bot_parsers = [
	'erpnext.utilities.bot.FindItemBot',
]

get_site_info = 'erpnext.utilities.get_site_info'
<<<<<<< HEAD

payment_gateway_enabled = "erpnext.accounts.utils.create_payment_gateway_account"

regional_overrides = {
	'India': {
		'erpnext.tests.test_regional.test_method': 'erpnext.regional.india.utils.test_method',
		'erpnext.controllers.taxes_and_totals.get_itemised_tax_breakup_header': 'erpnext.regional.india.utils.get_itemised_tax_breakup_header',
		'erpnext.controllers.taxes_and_totals.get_itemised_tax_breakup_data': 'erpnext.regional.india.utils.get_itemised_tax_breakup_data'
	}
}
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
