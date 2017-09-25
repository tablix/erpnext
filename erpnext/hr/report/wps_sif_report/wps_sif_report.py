# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint
from frappe import _

def execute(filters=None):
	if not filters: filters ={}

	month = filters.get("month")
	year = filters.get("year")

	if cint(month) < 1 and cint(month) > 12 :
		frappe.throw(_("'Month' must cannot be greater than 12  and less that 1"))

	columns = get_columns()
	employees  = get_emp_details(month, year)

	data = []
	for emp in employees:
		data.append(emp)
	return columns, data

def get_emp_details(month, year):
	return frappe.db.sql("""select
			emp.employee_unique_id as 'Employee Unique ID',
			emp.agent_id as 'Agent ID',
			emp.bank_ac_no as 'Employee Account With Agent',
			ss.net_pay as 'Income Fixed Component',
			0.00 as 'Income Variable Component',
			0.00 as 'Days On Leave without pay For the period',
			ss.start_date as 'Pay Start Date',
			ss.end_date as 'Pay End Date',
			ss.total_days_in_month as 'Salary Payable Days For the period',
			0.00 as 'Variable Pay Code - 1',
			0.00 as 'Variable Pay Amount -1',
			0.00 as 'Variable Pay Code - 2',
			0.00 as 'Variable Pay Amount -2',
			0.00 as 'Variable Pay Code - 3',
			0.00 as 'Variable Pay Amount -3'
		from `tabEmployee` emp
		inner join `tabSalary Slip` ss
		on emp.name = ss.employee
		where ss.month = {0}
		and ss.fiscal_year = {1}
		order by emp.name desc """.format(month,year), as_list=1)

def get_columns():
	return [
		_("Employee Unique ID") + "::160",
		_("Agent ID") + ":Data:120",	
		_("Employee Account With Agent") + "::120",
		_("Income Fixed Component") + ":Currency:120",
		_("Income Variable Component") + ":Currency:120",
		_("Days On Leave without pay For the period") + ":Currency:120",
		_("Pay Start Date") + ":Date:160",
		_("Pay End Date") + ":Date:160",
		_("Salary Payable Days For the period") + ":Data:160",
		_("Variable Pay Code - 1") + ":Currency:120",
		_("Variable Pay Amount -1") + ":Currency:120",
		_("Variable Pay Code - 2") + ":Currency:120",
		_("Variable Pay Amount -2") + ":Currency:120",
		_("Variable Pay Code - 3") + ":Currency:120",
		_("Variable Pay Amount -3") + ":Currency:120"
	]
