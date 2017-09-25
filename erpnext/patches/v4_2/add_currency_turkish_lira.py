# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
<<<<<<< HEAD

def execute():
	return
	# country = get_country_info(country="Turkey")
	# add_country_and_currency("Turkey", country)
=======
from frappe.geo.country_info import get_country_info
from erpnext.setup.install import add_country_and_currency

def execute():
	country = get_country_info(country="Turkey")
	add_country_and_currency("Turkey", country)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
