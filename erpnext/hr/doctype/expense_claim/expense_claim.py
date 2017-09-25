# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
<<<<<<< HEAD
from frappe import _
from frappe.utils import get_fullname, flt, cstr
from frappe.model.document import Document
from erpnext.hr.utils import set_employee_name
from erpnext.accounts.party import get_party_account
from erpnext.accounts.general_ledger import make_gl_entries
from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account
from erpnext.controllers.accounts_controller import AccountsController
from frappe.utils.csvutils import getlink

class InvalidExpenseApproverError(frappe.ValidationError): pass

class ExpenseClaim(AccountsController):
	def onload(self):
		self.get("__onload").make_payment_via_journal_entry = frappe.db.get_single_value('Accounts Settings', 
			'make_payment_via_journal_entry')

=======
from frappe import _, msgprint
from frappe.utils import get_fullname, flt, cint, round_based_on_smallest_currency_fraction, get_link_to_form, money_in_words
from frappe.model.document import Document
from erpnext.hr.utils import set_employee_name
from frappe.desk.form import assign_to

class InvalidExpenseApproverError(frappe.ValidationError): pass

class ExpenseClaim(Document):
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def get_feed(self):
		return _("{0}: From {0} for {1}").format(self.approval_status,
			self.employee_name, self.total_claimed_amount)

	def validate(self):
		self.validate_sanctioned_amount()
		self.validate_expense_approver()
		self.calculate_total_amount()
		set_employee_name(self)
		self.set_expense_account()
<<<<<<< HEAD
		self.set_payable_account()
		self.set_cost_center()
		self.set_status()
		self.validate_advance_payment()
		if self.task and not self.project:
			self.project = frappe.db.get_value("Task", self.task, "project")

	def set_status(self):
		self.status = {
			"0": "Draft",
			"1": "Submitted",
			"2": "Cancelled"
		}[cstr(self.docstatus or 0)]

		total_paid_amount = flt(self.total_amount_reimbursed) + flt(self.total_advance_paid)
		if self.total_sanctioned_amount > 0 and self.total_sanctioned_amount == total_paid_amount \
			and self.docstatus == 1 and self.approval_status == 'Approved':
			self.status = "Paid"
		elif self.total_sanctioned_amount > 0 and self.docstatus == 1 and self.approval_status == 'Approved':
			self.status = "Unpaid"
		elif self.docstatus == 1 and self.approval_status == 'Rejected':
			self.status = 'Rejected'

	def set_payable_account(self):
		if not self.payable_account and not self.is_paid:
			self.payable_account = frappe.db.get_value("Company", self.company, "default_payable_account")

	def set_cost_center(self):
		if not self.cost_center:
			self.cost_center = frappe.db.get_value('Company', self.company, 'cost_center')
=======
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
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	def on_submit(self):
		if self.approval_status=="Draft":
			frappe.throw(_("""Approval Status must be 'Approved' or 'Rejected'"""))
<<<<<<< HEAD

		self.update_task_and_project()
		self.make_gl_entries()

		if self.is_paid:
			update_paid_amount(self, self.payable_account)

		self.set_status()

	def on_cancel(self):
		self.update_task_and_project()
		if self.payable_account:
			self.make_gl_entries(cancel=True)

		if self.is_paid:
			update_paid_amount(self, self.payable_account)

		self.set_status()
=======
		self.update_task_and_project()

	def on_cancel(self):
		self.update_task_and_project()
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	def update_task_and_project(self):
		if self.task:
			self.update_task()
		elif self.project:
			frappe.get_doc("Project", self.project).update_project()

<<<<<<< HEAD
	def make_gl_entries(self, cancel = False):
		if flt(self.total_sanctioned_amount) > 0:
			gl_entries = self.get_gl_entries()
			make_gl_entries(gl_entries, cancel)

	def get_gl_entries(self):
		gl_entry = []
		self.validate_account_details()
		
		outstanding_amount = flt(self.total_sanctioned_amount) - flt(self.total_advance_paid)

		# payable entry
		if outstanding_amount:
			gl_entry.append(
				self.get_gl_dict({
					"account": self.payable_account,
					"credit": outstanding_amount,
					"credit_in_account_currency": outstanding_amount,
					"against": ",".join([d.default_account for d in self.expenses]),
					"party_type": "Employee",
					"party": self.employee,
					"against_voucher_type": self.doctype,
					"against_voucher": self.name
				})
			)

		if self.total_advance_paid:
			gl_entry.append(
				self.get_gl_dict({
					"account": self.advance_account,
					"credit": self.total_advance_paid,
					"credit_in_account_currency": self.total_advance_paid,
					"against": ",".join([d.default_account for d in self.expenses]),
					"party_type": "Employee",
					"party": self.employee,
					"against_voucher_type": self.doctype,
					"against_voucher": self.name
				})
			)

		# expense entries
		for data in self.expenses:
			gl_entry.append(
				self.get_gl_dict({
					"account": data.default_account,
					"debit": data.sanctioned_amount,
					"debit_in_account_currency": data.sanctioned_amount,
					"against": self.employee,
					"cost_center": self.cost_center
				})
			)

		if self.is_paid and outstanding_amount:
			# payment entry
			payment_account = get_bank_cash_account(self.mode_of_payment, self.company).get("account")

			gl_entry.append(
				self.get_gl_dict({
					"account": payment_account,
					"credit": outstanding_amount,
					"credit_in_account_currency": outstanding_amount,
					"against": self.employee
				})
			)

			gl_entry.append(
				self.get_gl_dict({
					"account": self.payable_account,
					"party_type": "Employee",
					"party": self.employee,
					"against": payment_account,
					"debit": outstanding_amount,
					"debit_in_account_currency": outstanding_amount,
					"against_voucher": self.name,
					"against_voucher_type": self.doctype,
				})
			)

		return gl_entry

	def validate_account_details(self):
		if not self.cost_center:
			frappe.throw(_("Cost center is required to book an expense claim"))

		if not self.payable_account:
			frappe.throw(_("Please set default payable account for the company {0}").format(getlink("Company",self.company)))

		if self.is_paid:
			if not self.mode_of_payment:
				frappe.throw(_("Mode of payment is required to make a payment").format(self.employee))

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def calculate_total_amount(self):
		self.total_claimed_amount = 0
		self.total_sanctioned_amount = 0
		for d in self.get('expenses'):
<<<<<<< HEAD
			if self.approval_status == 'Rejected':
				d.sanctioned_amount = 0.0

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
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
<<<<<<< HEAD
				expense.default_account = get_expense_claim_account(expense.expense_type,
					self.company)["account"]

	def validate_advance_payment(self):
		if self.advance_required:
			if self.docstatus == 1 and not self.total_advance_paid:
				frappe.throw(_("Advance payment required before submission of the Expense Claim"))
		elif self.total_advance_paid:
			frappe.throw(_("As advance payment already done, cannot unset 'Advance Payment Required'"))

def update_paid_amount(doc, party_account):
	paid_amount = frappe.db.sql("""
		select ifnull(sum(debit_in_account_currency), 0) as amount
		from `tabGL Entry`
		where 
			against_voucher_type = 'Expense Claim' and against_voucher = %s
			and party = %s and account = %s
	""", (doc.name, doc.employee, party_account) ,as_dict=1)[0].amount

	paid_amount_field = None
	if party_account == doc.payable_account:
		paid_amount_field = "total_amount_reimbursed"
	elif party_account == doc.advance_account:
		paid_amount_field = "total_advance_paid"

	if paid_amount_field:
		doc.set(paid_amount_field, paid_amount)
		frappe.db.set_value("Expense Claim", doc.name , paid_amount_field, paid_amount)

		doc.set_status()
		frappe.db.set_value("Expense Claim", doc.name , "status", doc.status)

=======
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

		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
@frappe.whitelist()
def get_expense_approver(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""
		select u.name, concat(u.first_name, ' ', u.last_name)
<<<<<<< HEAD
		from tabUser u, `tabHas Role` r
=======
		from tabUser u, tabUserRole r
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		where u.name = r.parent and r.role = 'Expense Approver' 
		and u.enabled = 1 and u.name like %s
	""", ("%" + txt + "%"))

@frappe.whitelist()
<<<<<<< HEAD
def make_bank_entry(dt, dn):
	from erpnext.accounts.doctype.journal_entry.journal_entry import get_default_bank_cash_account

	expense_claim = frappe.get_doc(dt, dn)
	default_bank_cash_account = get_default_bank_cash_account(expense_claim.company, "Bank")
	if not default_bank_cash_account:
		default_bank_cash_account = get_default_bank_cash_account(expense_claim.company, "Cash")

	if expense_claim.docstatus == 0:
		party_account = expense_claim.advance_account
	else:
		party_account = expense_claim.payable_account

	payment_amount = flt(expense_claim.total_sanctioned_amount) \
		- flt(expense_claim.total_amount_reimbursed) - flt(expense_claim.total_advance_paid)
=======
def make_bank_entry(docname):
	from erpnext.accounts.doctype.journal_entry.journal_entry import get_default_bank_cash_account

	expense_claim = frappe.get_doc("Expense Claim", docname)
	default_bank_cash_account = get_default_bank_cash_account(expense_claim.company, "Bank")
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	je = frappe.new_doc("Journal Entry")
	je.voucher_type = 'Bank Entry'
	je.company = expense_claim.company
<<<<<<< HEAD
	je.remark = 'Advance ' if expense_claim.docstatus==0 else '' + 'Payment against Expense Claim: ' + dn;

	je.append("accounts", {
		"account": party_account,
		"debit_in_account_currency": payment_amount,
		"reference_type": "Expense Claim",
		"reference_name": expense_claim.name,
		"party_type": "Employee",
		"party": expense_claim.employee
	})

	je.append("accounts", {
		"account": default_bank_cash_account.account,
		"credit_in_account_currency": payment_amount,
=======
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
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
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