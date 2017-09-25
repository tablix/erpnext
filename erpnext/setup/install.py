# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

<<<<<<< HEAD
from __future__ import print_function, unicode_literals

import frappe
from frappe import _
from frappe.desk.page.setup_wizard.setup_wizard import add_all_roles_to
from frappe.custom.doctype.custom_field.custom_field import create_custom_field
=======
from __future__ import unicode_literals

import frappe
from frappe import _
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

default_mail_footer = """<div style="padding: 7px; text-align: right; color: #888"><small>Sent via
	<a style="color: #888" href="http://erpnext.org">ERPNext</a></div>"""

def after_install():
	frappe.get_doc({'doctype': "Role", "role_name": "Analytics"}).insert()
	set_single_defaults()
	create_compact_item_print_custom_field()
<<<<<<< HEAD
	create_print_zero_amount_taxes_custom_field()
=======
	from frappe.desk.page.setup_wizard.setup_wizard import add_all_roles_to
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	add_all_roles_to("Administrator")
	frappe.db.commit()

def check_setup_wizard_not_completed():
	if frappe.db.get_default('desktop:home_page') == 'desktop':
<<<<<<< HEAD
		print()
		print("ERPNext can only be installed on a fresh site where the setup wizard is not completed")
		print("You can reinstall this site (after saving your data) using: bench --site [sitename] reinstall")
		print()
		return False

def set_single_defaults():
	for dt in ('Accounts Settings', 'Print Settings', 'HR Settings', 'Buying Settings',
		'Selling Settings', 'Stock Settings', 'Daily Work Summary Settings'):
=======
		print
		print "ERPNext can only be installed on a fresh site where the setup wizard is not completed"
		print "You can reinstall this site (after saving your data) using: bench --site [sitename] reinstall"
		print
		return False

def set_single_defaults():
	for dt in frappe.db.sql_list("""select name from `tabDocType` where issingle=1"""):
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		default_values = frappe.db.sql("""select fieldname, `default` from `tabDocField`
			where parent=%s""", dt)
		if default_values:
			try:
				b = frappe.get_doc(dt, dt)
				for fieldname, value in default_values:
					b.set(fieldname, value)
				b.save()
			except frappe.MandatoryError:
				pass
<<<<<<< HEAD
			except frappe.ValidationError:
				pass
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	frappe.db.set_default("date_format", "dd-mm-yyyy")

def create_compact_item_print_custom_field():
<<<<<<< HEAD
=======
	from frappe.custom.doctype.custom_field.custom_field import create_custom_field
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	create_custom_field('Print Settings', {
		'label': _('Compact Item Print'),
		'fieldname': 'compact_item_print',
		'fieldtype': 'Check',
		'default': 1,
		'insert_after': 'with_letterhead'
<<<<<<< HEAD
	})

def create_print_zero_amount_taxes_custom_field():
	create_custom_field('Print Settings', {
		'label': _('Print taxes with zero amount'),
		'fieldname': 'print_taxes_with_zero_amount',
		'fieldtype': 'Check',
		'default': 0,
		'insert_after': 'allow_print_for_cancelled'
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	})