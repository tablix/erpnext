# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

<<<<<<< HEAD
from frappe.utils import flt, cint, getdate
=======
from frappe.utils import cstr, flt, getdate
from frappe.model.naming import make_autoname
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document
from erpnext.hr.utils import set_employee_name

class SalaryStructure(Document):
<<<<<<< HEAD
	
	def validate(self):
		self.validate_amount()
		for e in self.get('employees'):
			set_employee_name(e)
		self.validate_date()
		self.strip_condition_and_formula_fields()
=======
	def autoname(self):
		self.name = make_autoname(self.employee + '/.SST' + '/.#####')
		
	def validate(self):
		self.check_overlap()
		self.validate_amount()
		self.validate_employee()
		self.validate_joining_date()
		set_employee_name(self)

	def get_employee_details(self):
		ret = {}
		det = frappe.db.sql("""select employee_name, branch, designation, department
			from `tabEmployee` where name = %s""", self.employee)
		if det:
			ret = {
				'employee_name': cstr(det[0][0]),
				'branch': cstr(det[0][1]),
				'designation': cstr(det[0][2]),
				'department': cstr(det[0][3]),
				'backup_employee': cstr(self.employee)
			}
		return ret
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	def get_ss_values(self,employee):
		basic_info = frappe.db.sql("""select bank_name, bank_ac_no
			from `tabEmployee` where name =%s""", employee)
		ret = {'bank_name': basic_info and basic_info[0][0] or '',
			'bank_ac_no': basic_info and basic_info[0][1] or ''}
		return ret

<<<<<<< HEAD
=======
	def make_table(self, doct_name, tab_fname, tab_name):
		list1 = frappe.db.sql("select name from `tab%s` where docstatus != 2" % doct_name)
		for li in list1:
			child = self.append(tab_fname, {})
			if(tab_fname == 'earnings'):
				child.salary_component = cstr(li[0])
				child.amount = 0
			elif(tab_fname == 'deductions'):
				child.salary_component = cstr(li[0])
				child.amount = 0

	def make_earn_ded_table(self):
		self.make_table('Salary Component','earnings','Salary Detail')
		self.make_table('Salary Component','deductions', 'Salary Detail')

	def check_overlap(self):
		existing = frappe.db.sql("""select name from `tabSalary Structure`
			where employee = %(employee)s and
			(
				(%(from_date)s > from_date and %(from_date)s < to_date) or
				(%(to_date)s > from_date and %(to_date)s < to_date) or
				(%(from_date)s <= from_date and %(to_date)s >= to_date))
			and name!=%(name)s
			and docstatus < 2""",
			{
				"employee": self.employee,
				"from_date": self.from_date,
				"to_date": self.to_date,
				"name": self.name or "No Name"
			}, as_dict=True)
			
		if existing:
			frappe.throw(_("Salary structure {0} already exist, more than one salary structure for same period is not allowed").format(existing[0].name))

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def validate_amount(self):
		if flt(self.net_pay) < 0 and self.salary_slip_based_on_timesheet:
			frappe.throw(_("Net pay cannot be negative"))

<<<<<<< HEAD
	def validate_date(self):
		for employee in self.get('employees'):
			joining_date, relieving_date = frappe.db.get_value("Employee", employee.employee,
				["date_of_joining", "relieving_date"])

			if employee.from_date and joining_date and getdate(employee.from_date) < joining_date:
				frappe.throw(_("From Date {0} for Employee {1} cannot be before employee's joining Date {2}")
					    .format(employee.from_date, employee.employee, joining_date))

		st_name = frappe.db.sql("""select parent from `tabSalary Structure Employee`
			where
			employee=%(employee)s
			and (
				(%(from_date)s between from_date and ifnull(to_date, '2199-12-31'))
				or (%(to_date)s between from_date and ifnull(to_date, '2199-12-31'))
				or (from_date between %(from_date)s and %(to_date)s)
			)
			and (
				exists (select name from `tabSalary Structure`
				where name = `tabSalary Structure Employee`.parent and is_active = 'Yes')
			)
			and parent != %(salary_struct)s""",
			{
				'employee': employee.employee,
				'from_date': employee.from_date,
				'to_date': (employee.to_date or '2199-12-31'),
				'salary_struct': self.name
			})

		if st_name:
			frappe.throw(_("Active Salary Structure {0} found for employee {1} for the given dates")
				.format(st_name[0][0], employee.employee))

	def strip_condition_and_formula_fields(self):
		# remove whitespaces from condition and formula fields
		for row in self.earnings:
			row.condition = row.condition.strip() if row.condition else ""
			row.formula = row.formula.strip() if row.formula else ""

		for row in self.deductions:
			row.condition = row.condition.strip() if row.condition else ""
			row.formula = row.formula.strip() if row.formula else ""

@frappe.whitelist()
def make_salary_slip(source_name, target_doc = None, employee = None, as_print = False, print_format = None):
	def postprocess(source, target):
		if employee:
			employee_details = frappe.db.get_value("Employee", employee, 
							["employee_name", "branch", "designation", "department"], as_dict=1)
			target.employee = employee
			target.employee_name = employee_details.employee_name
			target.branch = employee_details.branch
			target.designation = employee_details.designation
			target.department = employee_details.department
		target.run_method('process_salary_structure')
=======
	def validate_employee(self):
		old_employee = frappe.db.get_value("Salary Structure", self.name, "employee")
		if old_employee and self.employee != old_employee:
			frappe.throw(_("Employee can not be changed"))

	def validate_joining_date(self):
		joining_date = getdate(frappe.db.get_value("Employee", self.employee, "date_of_joining"))
		if getdate(self.from_date) < joining_date:
			frappe.throw(_("From Date in Salary Structure cannot be lesser than Employee Joining Date."))

@frappe.whitelist()
def make_salary_slip(source_name, target_doc=None):
	def postprocess(source, target):
		# copy earnings and deductions table
		for key in ('earnings', 'deductions'):
			for d in source.get(key):
				target.append(key, {
					'amount': d.amount,
					'default_amount': d.amount,
					'depends_on_lwp' : d.depends_on_lwp,
					'salary_component' : d.salary_component
				})

		target.run_method("pull_emp_details")
		target.run_method("get_leave_details")
		target.run_method("calculate_net_pay")
			
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	doc = get_mapped_doc("Salary Structure", source_name, {
		"Salary Structure": {
			"doctype": "Salary Slip",
			"field_map": {
				"total_earning": "gross_pay",
				"name": "salary_structure"
			}
		}
	}, target_doc, postprocess, ignore_child_tables=True)

<<<<<<< HEAD
	if cint(as_print):
		doc.name = 'Preview for {0}'.format(employee)
		return frappe.get_print(doc.doctype, doc.name, doc = doc, print_format = print_format)
	else:
		return doc


@frappe.whitelist()
def get_employees(**args):
	return frappe.get_list('Employee',filters=args['filters'], fields=['name', 'employee_name'])
=======
	return doc
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
