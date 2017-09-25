# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

<<<<<<< HEAD
from __future__ import print_function, unicode_literals
=======
from __future__ import unicode_literals
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
from frappe.permissions import reset_perms

def execute():
	for doctype in ("About Us Settings", "Accounts Settings", "Activity Type",
		"Blog Category", "Blog Settings", "Blogger", "Branch", "Brand", "Buying Settings",
		"Communication", "Company", "Contact Us Settings",
		"Country", "Currency", "Currency Exchange", "Deduction Type", "Department",
		"Designation", "Earning Type", "Event", "Feed", "File", "Fiscal Year",
		"HR Settings", "Industry Type", "Leave Type", "Letter Head",
		"Mode of Payment", "Module Def", "Naming Series", "POS Setting", "Print Heading",
		"Report", "Role", "Selling Settings", "Stock Settings", "Supplier Type", "UOM"):
		try:
			reset_perms(doctype)
		except:
<<<<<<< HEAD
			print("Error resetting perms for", doctype)
=======
			print "Error resetting perms for", doctype
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			raise
