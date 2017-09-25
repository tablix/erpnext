# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt"


from __future__ import unicode_literals
import frappe

def boot_session(bootinfo):
	"""boot session - send website info if guest"""
<<<<<<< HEAD
=======
	import frappe
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	bootinfo.custom_css = frappe.db.get_value('Style Settings', None, 'custom_css') or ''
	bootinfo.website_settings = frappe.get_doc('Website Settings')

	if frappe.session['user']!='Guest':
<<<<<<< HEAD
		update_page_info(bootinfo)

		load_country_and_currency(bootinfo)
		bootinfo.sysdefaults.territory = frappe.db.get_single_value('Selling Settings',
			'territory')
		bootinfo.sysdefaults.customer_group = frappe.db.get_single_value('Selling Settings',
			'customer_group')
=======
		bootinfo.letter_heads = get_letter_heads()

		update_page_info(bootinfo)

		load_country_and_currency(bootinfo)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

		bootinfo.notification_settings = frappe.get_doc("Notification Control",
			"Notification Control")

		# if no company, show a dialog box to create a new company
		bootinfo.customer_count = frappe.db.sql("""select count(*) from tabCustomer""")[0][0]

		if not bootinfo.customer_count:
			bootinfo.setup_complete = frappe.db.sql("""select name from
				tabCompany limit 1""") and 'Yes' or 'No'

<<<<<<< HEAD
		bootinfo.docs += frappe.db.sql("""select name, default_currency, cost_center, default_terms,
			default_letter_head, default_bank_account, enable_perpetual_inventory from `tabCompany`""",
=======
		bootinfo.docs += frappe.db.sql("""select name, default_currency, cost_center,
			default_terms, default_letter_head, default_bank_account from `tabCompany`""",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			as_dict=1, update={"doctype":":Company"})

def load_country_and_currency(bootinfo):
	country = frappe.db.get_default("country")
	if country and frappe.db.exists("Country", country):
		bootinfo.docs += [frappe.get_doc("Country", country)]

	bootinfo.docs += frappe.db.sql("""select name, fraction, fraction_units,
		number_format, smallest_currency_fraction_value, symbol from tabCurrency
		where enabled=1""", as_dict=1, update={"doctype":":Currency"})

<<<<<<< HEAD
=======
def get_letter_heads():
	import frappe
	ret = frappe.db.sql("""select name, content from `tabLetter Head`
		where disabled=0""")
	return dict(ret)

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
def update_page_info(bootinfo):
	bootinfo.page_info.update({
		"Chart of Accounts": {
			"title": "Chart of Accounts",
			"route": "Tree/Account"
		},
		"Chart of Cost Centers": {
			"title": "Chart of Cost Centers",
			"route": "Tree/Cost Center"
		},
		"Item Group Tree": {
			"title": "Item Group Tree",
			"route": "Tree/Item Group"
		},
		"Customer Group Tree": {
			"title": "Customer Group Tree",
			"route": "Tree/Customer Group"
		},
		"Territory Tree": {
			"title": "Territory Tree",
			"route": "Tree/Territory"
		},
		"Sales Person Tree": {
			"title": "Sales Person Tree",
			"route": "Tree/Sales Person"
		}
	})
