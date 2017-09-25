# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint
from frappe.utils import get_fullname, flt, cint, round_based_on_smallest_currency_fraction, get_link_to_form, money_in_words
from frappe.model.document import Document
from erpnext.hr.utils import set_employee_name
from frappe.desk.form import assign_to

class InvalidExpenseApproverError(frappe.ValidationError): pass

class ExpenseClaim(Document):
	def get_feed(self):
		return _("{0}: From {0} for {1}").format(self.approval_status,
			self.employee_name, self.total_claimed_amount)

	def validate(self):
		self.validate_sanctioned_amount()
		self.validate_expense_approver()
		self.calculate_total_amount()
		set_employee_name(self)
		self.set_expense_account()
		if self.task and not self.project:
			self.project = frappe.db.get_value("Task", self.task, "project")
		#new addition
		#if self.assigned == 0: 
		#	if self.exp_approver:
		#		self.assign_to_expense_approver()
		#else:
		#	if self.exp_approver != self.prev_approver:
		#		self.assign_to_expense_approver()
		if (self.approval_status == "Approved" or self.approval_status == "Rejected") and self.assigned == 1:
			self.validate_approval_rejection_status()

	def on_submit(self):
		if self.approval_status=="Draft":
			frappe.throw(_("""Approval Status must be 'Approved' or 'Rejected'"""))
		self.update_task_and_project()

	def on_cancel(self):
		self.update_task_and_project()

	def update_task_and_project(self):
		if self.task:
			self.update_task()
		elif self.project:
			frappe.get_doc("Project", self.project).update_project()

	def calculate_total_amount(self):
		self.total_claimed_amount = 0
		self.total_sanctioned_amount = 0
		for d in self.get('expenses'):
			self.total_claimed_amount += flt(d.claim_amount)
			self.total_sanctioned_amount += flt(d.sanctioned_amount)

	def validate_expense_approver(self):
		if self.exp_approver and "Expense Approver" not in frappe.get_roles(self.exp_approver):
			frappe.throw(_("{0} ({1}) must have role 'Expense Approver'")\
				.format(get_fullname(self.exp_approver), self.exp_approver), InvalidExpenseApproverError)

	def update_task(self):
		task = frappe.get_doc("Task", self.task)
		task.update_total_expense_claim()
		task.save()

	def validate_sanctioned_amount(self):
		for d in self.get('expenses'):
			if flt(d.sanctioned_amount) > flt(d.claim_amount):
				frappe.throw(_("Sanctioned Amount cannot be greater than Claim Amount in Row {0}.").format(d.idx))

	def set_expense_account(self):
		for expense in self.expenses:
			if not expense.default_account:
				expense.default_account = get_expense_claim_account(expense.expense_type, self.company)["account"]
				
				
	#new addition
	
	def validate_approval_rejection_status(self):
		emp = self.employee
		emp_name = self.employee_name
		emp_email = frappe.get_value("Employee", emp, "user_id")
		if self.approval_status == "Approved":
			val = 1
		elif self.approval_status == "Rejected":
			val = 2
		self.notify_employee(emp_email, emp_name, val)
		self.assigned = 0
	
	
	def assign_to_expense_approver(self):
		emp_name = self.employee_name
		expense_approver = self.exp_approver
		val = 0
		self.notify_employee(expense_approver, emp_name, val)
		self.prev_approver = expense_approver
		frappe.db.set_value('Expense Claim', self.name, 'assigned', 1)
		frappe.db.commit()
	
	def notify_employee(self, employee, employee_name, val):
		
		#msgprint("Success" + str(val))
		
		def _get_message(url=False):
			if url:
				name = get_link_to_form(self.doctype, self.name)
			else:
				name = self.name
			if val == 0:
				return (_("Expense Claim")+ "- of %s " + _("assigned for Approval") + ": %s") % (employee_name, name)
			elif val ==1:
				return (_("Expense Claim has been Approved") + ": %s") % (name)
			elif val == 2:
				return (_("Expense Claim has been Rejected") + ": %s") % (name)
			
			
		self.notify({
			# for post in messages
			"message": _get_message(url=True),
			"message_to": employee,
			"subject": _get_message(),#
		})
	
		desc = ''	
		if val == 0:
			assign_to.clear(self.doctype, self.name)
			desc = "Expense Claim of " + str(employee) + " assigned for Approval"
			assign_to.add({
				"assign_to": employee,
				"doctype": self.doctype,
				"name": self.name,
				"description": desc
				})
		else:
			#msgprint("success")
			assign_to.clear(self.doctype, self.name)
		
		
	def notify(self, args):
		args = frappe._dict(args)
		from frappe.desk.page.chat.chat import post
		post(**{"txt": args.message, "contact": args.message_to, "subject": args.subject, "notify": 1})

		
@frappe.whitelist()
def get_expense_approver(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""
		select u.name, concat(u.first_name, ' ', u.last_name)
		from tabUser u, tabUserRole r
		where u.name = r.parent and r.role = 'Expense Approver' 
		and u.enabled = 1 and u.name like %s
	""", ("%" + txt + "%"))

@frappe.whitelist()
def make_bank_entry(docname):
	from erpnext.accounts.doctype.journal_entry.journal_entry import get_default_bank_cash_account

	expense_claim = frappe.get_doc("Expense Claim", docname)
	default_bank_cash_account = get_default_bank_cash_account(expense_claim.company, "Bank")

	je = frappe.new_doc("Journal Entry")
	je.voucher_type = 'Bank Entry'
	je.company = expense_claim.company
	je.remark = 'Payment against Expense Claim: ' + docname;

	for expense in expense_claim.expenses:
		je.append("accounts", {
			"account": expense.default_account,
			"debit_in_account_currency": expense.sanctioned_amount,
			"reference_type": "Expense Claim",
			"reference_name": expense_claim.name
		})

	je.append("accounts", {
		"account": default_bank_cash_account.account,
		"credit_in_account_currency": expense_claim.total_sanctioned_amount,
		"reference_type": "Expense Claim",
		"reference_name": expense_claim.name,
		"balance": default_bank_cash_account.balance,
		"account_currency": default_bank_cash_account.account_currency,
		"account_type": default_bank_cash_account.account_type
	})

	return je.as_dict()

@frappe.whitelist()
def get_expense_claim_account(expense_claim_type, company):
	account = frappe.db.get_value("Expense Claim Account",
		{"parent": expense_claim_type, "company": company}, "default_account")
	
	if not account:
		frappe.throw(_("Please set default account in Expense Claim Type {0}")
			.format(expense_claim_type))
	
	return {
		"account": account
	}