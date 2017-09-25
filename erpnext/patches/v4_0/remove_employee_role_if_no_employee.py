# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import frappe.permissions

def execute():
<<<<<<< HEAD
	for user in frappe.db.sql_list("select distinct parent from `tabHas Role` where role='Employee'"):
=======
	for user in frappe.db.sql_list("select distinct parent from `tabUserRole` where role='Employee'"):
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		# if employee record does not exists, remove employee role!
		if not frappe.db.get_value("Employee", {"user_id": user}):
			try:
				user = frappe.get_doc("User", user)
<<<<<<< HEAD
				for role in user.get("roles", {"role": "Employee"}):
					user.get("roles").remove(role)
=======
				for role in user.get("user_roles", {"role": "Employee"}):
					user.get("user_roles").remove(role)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				user.save()
			except frappe.DoesNotExistError:
				pass
