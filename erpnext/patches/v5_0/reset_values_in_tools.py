# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

def execute():
	for dt in ["Payment Tool", "Bank Reconciliation", "Payment Reconciliation", "Leave Control Panel", 
<<<<<<< HEAD
		"Salary Manager", "Upload Attenadance", "Production Planning Tool", "BOM Update Tool", "Customize Form",
		 "Employee Attendance Tool", "Rename Tool", "BOM Update Tool", "Process Payroll", "Naming Series"]:
=======
		"Salary Manager", "Upload Attenadance", "Production Planning Tool", "BOM Replace Tool", "Customize Form",
		 "Employee Attendance Tool", "Rename Tool", "BOM Replace Tool", "Process Payroll", "Naming Series"]:
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			frappe.db.sql("delete from `tabSingles` where doctype=%s", dt)
		