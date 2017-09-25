# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

<<<<<<< HEAD
from __future__ import print_function, unicode_literals
=======
from __future__ import unicode_literals
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
import frappe

def execute():
	country = frappe.db.get_single_value("Global Defaults", "country")
	if not country:
<<<<<<< HEAD
		print("Country not specified in Global Defaults")
=======
		print "Country not specified in Global Defaults"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		return

	for company in frappe.db.sql_list("""select name from `tabCompany`
		where ifnull(country, '')=''"""):
		frappe.db.set_value("Company", company, "country", country)
