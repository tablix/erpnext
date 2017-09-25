# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe import _, scrub, ValidationError
from frappe.utils import flt, comma_or, nowdate
from erpnext.accounts.utils import get_outstanding_invoices, get_account_currency, get_balance_on
from erpnext.accounts.party import get_party_account
from erpnext.accounts.doctype.journal_entry.journal_entry \
	import get_average_exchange_rate, get_default_bank_cash_account
from erpnext.setup.utils import get_exchange_rate
from erpnext.accounts.general_ledger import make_gl_entries
<<<<<<< HEAD
from erpnext.hr.doctype.expense_claim.expense_claim import update_paid_amount
=======

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
from erpnext.controllers.accounts_controller import AccountsController

class InvalidPaymentEntry(ValidationError): pass

class PaymentEntry(AccountsController):
<<<<<<< HEAD
	def setup_party_account_field(self):
		self.party_account_field = None
		self.party_account = None
		self.party_account_currency = None

=======
	def setup_party_account_field(self):		
		self.party_account_field = None
		self.party_account = None
		self.party_account_currency = None
		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		if self.payment_type == "Receive":
			self.party_account_field = "paid_from"
			self.party_account = self.paid_from
			self.party_account_currency = self.paid_from_account_currency
<<<<<<< HEAD

=======
			
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		elif self.payment_type == "Pay":
			self.party_account_field = "paid_to"
			self.party_account = self.paid_to
			self.party_account_currency = self.paid_to_account_currency
<<<<<<< HEAD

=======
							
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def validate(self):
		self.setup_party_account_field()
		self.set_missing_values()
		self.validate_payment_type()
		self.validate_party_details()
		self.validate_bank_accounts()
		self.set_exchange_rate()
		self.validate_mandatory()
		self.validate_reference_documents()
		self.set_amounts()
		self.clear_unallocated_reference_document_rows()
		self.validate_payment_against_negative_invoice()
		self.validate_transaction_reference()
		self.set_title()
		self.set_remarks()
<<<<<<< HEAD
		self.validate_duplicate_entry()
		self.validate_allocated_amount()

=======
		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def on_submit(self):
		self.setup_party_account_field()
		if self.difference_amount:
			frappe.throw(_("Difference Amount must be zero"))
		self.make_gl_entries()
		self.update_advance_paid()
<<<<<<< HEAD
		self.update_expense_claim()

=======
		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def on_cancel(self):
		self.setup_party_account_field()
		self.make_gl_entries(cancel=1)
		self.update_advance_paid()
<<<<<<< HEAD
		self.update_expense_claim()
		self.delink_advance_entry_references()

	def validate_duplicate_entry(self):
		reference_names = []
		for d in self.get("references"):
			if (d.reference_doctype, d.reference_name) in reference_names:
				frappe.throw(_("Row #{0}: Duplicate entry in References {1} {2}").format(d.idx, d.reference_doctype, d.reference_name))
			reference_names.append((d.reference_doctype, d.reference_name))


	def validate_allocated_amount(self):
		for d in self.get("references"):
			if (flt(d.allocated_amount))> 0:
				if flt(d.allocated_amount) > flt(d.outstanding_amount):
					frappe.throw(_("Row #{0}: Allocated Amount cannot be greater than outstanding amount.").format(d.idx))


	def delink_advance_entry_references(self):
		for reference in self.references:
			if reference.reference_doctype in ("Sales Invoice", "Purchase Invoice"):
				doc = frappe.get_doc(reference.reference_doctype, reference.reference_name)
				doc.delink_advance_entries(self.name)

	def set_missing_values(self):
		if self.payment_type == "Internal Transfer":
			for field in ("party", "party_balance", "total_allocated_amount",
=======
							
	def set_missing_values(self):
		if self.payment_type == "Internal Transfer":
			for field in ("party", "party_balance", "total_allocated_amount", 
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				"base_total_allocated_amount", "unallocated_amount"):
					self.set(field, None)
			self.references = []
		else:
			if not self.party_type:
				frappe.throw(_("Party Type is mandatory"))
<<<<<<< HEAD

			if not self.party:
				frappe.throw(_("Party is mandatory"))

			_party_name = "title" if self.party_type == "Student" else self.party_type.lower() + "_name"
			self.party_name = frappe.db.get_value(self.party_type, self.party, _party_name)

=======
				
			if not self.party:
				frappe.throw(_("Party is mandatory"))
				
			self.party_name = frappe.db.get_value(self.party_type, self.party, 
				self.party_type.lower() + "_name")
		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		if self.party:
			if not self.party_balance:
				self.party_balance = get_balance_on(party_type=self.party_type,
					party=self.party, date=self.posting_date, company=self.company)
<<<<<<< HEAD

=======
			
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			if not self.party_account:
				party_account = get_party_account(self.party_type, self.party, self.company)
				self.set(self.party_account_field, party_account)
				self.party_account = party_account
<<<<<<< HEAD

=======
				
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		if self.paid_from and not (self.paid_from_account_currency or self.paid_from_account_balance):
			acc = get_account_details(self.paid_from, self.posting_date)
			self.paid_from_account_currency = acc.account_currency
			self.paid_from_account_balance = acc.account_balance
<<<<<<< HEAD

=======
				
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		if self.paid_to and not (self.paid_to_account_currency or self.paid_to_account_balance):
			acc = get_account_details(self.paid_to, self.posting_date)
			self.paid_to_account_currency = acc.account_currency
			self.paid_to_account_balance = acc.account_balance
<<<<<<< HEAD

		self.party_account_currency = self.paid_from_account_currency \
			if self.payment_type=="Receive" else self.paid_to_account_currency

		self.set_missing_ref_details()


	def set_missing_ref_details(self):
		for d in self.get("references"):
			if d.allocated_amount:
				ref_details = get_reference_details(d.reference_doctype,
					d.reference_name, self.party_account_currency)

				for field, value in ref_details.items():
					if not d.get(field):
						d.set(field, value)

	def validate_payment_type(self):
		if self.payment_type not in ("Receive", "Pay", "Internal Transfer"):
			frappe.throw(_("Payment Type must be one of Receive, Pay and Internal Transfer"))

=======
			
		self.party_account_currency = self.paid_from_account_currency \
			if self.payment_type=="Receive" else self.paid_to_account_currency
			
		self.set_missing_ref_details()
			
	
	def set_missing_ref_details(self):
		for d in self.get("references"):
			if d.allocated_amount:
				ref_details = get_reference_details(d.reference_doctype, 
					d.reference_name, self.party_account_currency)
					
				for field, value in ref_details.items():
					if not d.get(field):
						d.set(field, value)
						
	def validate_payment_type(self):
		if self.payment_type not in ("Receive", "Pay", "Internal Transfer"):
			frappe.throw(_("Payment Type must be one of Receive, Pay and Internal Transfer"))
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def validate_party_details(self):
		if self.party:
			if not frappe.db.exists(self.party_type, self.party):
				frappe.throw(_("Invalid {0}: {1}").format(self.party_type, self.party))
<<<<<<< HEAD

			if self.party_account:
				party_account_type = "Receivable" if self.party_type in ("Customer", "Student") else "Payable"
				self.validate_account_type(self.party_account, [party_account_type])

	def validate_bank_accounts(self):
		if self.payment_type in ("Pay", "Internal Transfer"):
			self.validate_account_type(self.paid_from, ["Bank", "Cash"])

		if self.payment_type in ("Receive", "Internal Transfer"):
			self.validate_account_type(self.paid_to, ["Bank", "Cash"])

=======
			
			if self.party_account:
				party_account_type = "Receivable" if self.party_type=="Customer" else "Payable"
				self.validate_account_type(self.party_account, [party_account_type])
					
	def validate_bank_accounts(self):
		if self.payment_type in ("Pay", "Internal Transfer"):
			self.validate_account_type(self.paid_from, ["Bank", "Cash"])
			
		if self.payment_type in ("Receive", "Internal Transfer"):
			self.validate_account_type(self.paid_to, ["Bank", "Cash"])
			
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def validate_account_type(self, account, account_types):
		account_type = frappe.db.get_value("Account", account, "account_type")
		if account_type not in account_types:
			frappe.throw(_("Account Type for {0} must be {1}").format(account, comma_or(account_types)))
<<<<<<< HEAD

=======
				
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def set_exchange_rate(self):
		if self.paid_from and not self.source_exchange_rate:
			if self.paid_from_account_currency == self.company_currency:
				self.source_exchange_rate = 1
<<<<<<< HEAD
			else:
				self.source_exchange_rate = get_exchange_rate(self.paid_from_account_currency,
					self.company_currency, self.posting_date)

		if self.paid_to and not self.target_exchange_rate:
			self.target_exchange_rate = get_exchange_rate(self.paid_to_account_currency,
				self.company_currency, self.posting_date)

=======
			elif self.payment_type in ("Pay", "Internal Transfer"):
				self.source_exchange_rate = get_average_exchange_rate(self.paid_from)
			else:
				self.source_exchange_rate = get_exchange_rate(self.paid_from_account_currency, 
					self.company_currency)
		
		if self.paid_to and not self.target_exchange_rate:
			self.target_exchange_rate = get_exchange_rate(self.paid_to_account_currency, 
				self.company_currency)
				
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def validate_mandatory(self):
		for field in ("paid_amount", "received_amount", "source_exchange_rate", "target_exchange_rate"):
			if not self.get(field):
				frappe.throw(_("{0} is mandatory").format(self.meta.get_label(field)))
<<<<<<< HEAD

	def validate_reference_documents(self):
		if self.party_type == "Student":
			valid_reference_doctypes = ("Fees")
		elif self.party_type == "Customer":
			valid_reference_doctypes = ("Sales Order", "Sales Invoice", "Journal Entry")
		elif self.party_type == "Supplier":
			valid_reference_doctypes = ("Purchase Order", "Purchase Invoice", "Journal Entry")
		elif self.party_type == "Employee":
			valid_reference_doctypes = ("Expense Claim", "Journal Entry")

=======
				
	def validate_reference_documents(self):
		if self.party_type == "Customer":
			valid_reference_doctypes = ("Sales Order", "Sales Invoice", "Journal Entry")
		else:
			valid_reference_doctypes = ("Purchase Order", "Purchase Invoice", "Journal Entry")
			
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		for d in self.get("references"):
			if not d.allocated_amount:
				continue
			if d.reference_doctype not in valid_reference_doctypes:
				frappe.throw(_("Reference Doctype must be one of {0}")
					.format(comma_or(valid_reference_doctypes)))
<<<<<<< HEAD

=======
				
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			elif d.reference_name:
				if not frappe.db.exists(d.reference_doctype, d.reference_name):
					frappe.throw(_("{0} {1} does not exist").format(d.reference_doctype, d.reference_name))
				else:
					ref_doc = frappe.get_doc(d.reference_doctype, d.reference_name)

					if d.reference_doctype != "Journal Entry":
						if self.party != ref_doc.get(scrub(self.party_type)):
							frappe.throw(_("{0} {1} does not associated with {2} {3}")
								.format(d.reference_doctype, d.reference_name, self.party_type, self.party))
					else:
						self.validate_journal_entry()
<<<<<<< HEAD

					if d.reference_doctype in ("Sales Invoice", "Purchase Invoice", "Expense Claim", "Fees"):
						if self.party_type == "Customer":
							ref_party_account = ref_doc.debit_to
						elif self.party_type == "Student":
							ref_party_account = ref_doc.receivable_account
						elif self.party_type=="Supplier":
							ref_party_account = ref_doc.credit_to
						elif self.party_type=="Employee":
							ref_party_account = ref_doc.payable_account \
								if ref_doc.docstatus==1 else ref_doc.advance_account

						if ref_party_account != self.party_account:
								frappe.throw(_("{0} {1} is associated with {2}, but Party Account is {3}")
									.format(d.reference_doctype, d.reference_name, ref_party_account, self.party_account))

					if ref_doc.docstatus != 1:
						if d.reference_doctype!="Expense Claim":
							frappe.throw(_("{0} {1} must be submitted")
								.format(d.reference_doctype, d.reference_name))
						elif not ref_doc.advance_required:
							frappe.throw(_("Advance Payment Required should be checked in Expense Claim {0}")
								.format(d.reference_name))

	def validate_journal_entry(self):
		for d in self.get("references"):
			if d.allocated_amount and d.reference_doctype == "Journal Entry":
=======
								
					if d.reference_doctype in ("Sales Invoice", "Purchase Invoice"):
						ref_party_account = ref_doc.debit_to \
							if self.party_type=="Customer" else ref_doc.credit_to
						if ref_party_account != self.party_account:
							frappe.throw(_("{0} {1} does not associated with Party Account {2}")
								.format(d.reference_doctype, d.reference_name, self.party_account))
						
					if ref_doc.docstatus != 1:
						frappe.throw(_("{0} {1} must be submitted")
							.format(d.reference_doctype, d.reference_name))
							
	def validate_journal_entry(self):
		for d in self.get("references"):
			if d.allocated_amount and d.reference_doctype == "Journal Entry":				
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				je_accounts = frappe.db.sql("""select debit, credit from `tabJournal Entry Account`
					where account = %s and party=%s and docstatus = 1 and parent = %s
					and (reference_type is null or reference_type in ("", "Sales Order", "Purchase Order"))
					""", (self.party_account, self.party, d.reference_name), as_dict=True)

				if not je_accounts:
					frappe.throw(_("Row #{0}: Journal Entry {1} does not have account {2} or already matched against another voucher")
						.format(d.idx, d.reference_name, self.party_account))
				else:
					dr_or_cr = "debit" if self.payment_type == "Receive" else "credit"
					valid = False
					for jvd in je_accounts:
						if flt(jvd[dr_or_cr]) > 0:
							valid = True
					if not valid:
						frappe.throw(_("Against Journal Entry {0} does not have any unmatched {1} entry")
							.format(d.reference_name, dr_or_cr))
<<<<<<< HEAD

=======
							
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def set_amounts(self):
		self.set_amounts_in_company_currency()
		self.set_total_allocated_amount()
		self.set_unallocated_amount()
		self.set_difference_amount()

	def set_amounts_in_company_currency(self):
		self.base_paid_amount, self.base_received_amount, self.difference_amount = 0, 0, 0
		if self.paid_amount:
<<<<<<< HEAD
			self.base_paid_amount = flt(flt(self.paid_amount) * flt(self.source_exchange_rate),
				self.precision("base_paid_amount"))

		if self.received_amount:
			self.base_received_amount = flt(flt(self.received_amount) * flt(self.target_exchange_rate),
				self.precision("base_received_amount"))

	def set_total_allocated_amount(self):
		if self.payment_type == "Internal Transfer":
			return

		total_allocated_amount, base_total_allocated_amount = 0, 0
		for d in self.get("references"):
			if d.allocated_amount:
				total_allocated_amount += flt(d.allocated_amount)
				base_total_allocated_amount += flt(flt(d.allocated_amount) * flt(d.exchange_rate),
					self.precision("base_paid_amount"))

		self.total_allocated_amount = abs(total_allocated_amount)
		self.base_total_allocated_amount = abs(base_total_allocated_amount)

=======
			self.base_paid_amount = flt(flt(self.paid_amount) * flt(self.source_exchange_rate), 
				self.precision("base_paid_amount"))
				
		if self.received_amount:
			self.base_received_amount = flt(flt(self.received_amount) * flt(self.target_exchange_rate), 
				self.precision("base_received_amount"))
				
	def set_total_allocated_amount(self):
		if self.payment_type == "Internal Transfer":
			return
			
		total_allocated_amount, base_total_allocated_amount = 0, 0
		for d in self.get("references"):
			if d.allocated_amount:				
				total_allocated_amount += flt(d.allocated_amount)
				base_total_allocated_amount += flt(flt(d.allocated_amount) * flt(d.exchange_rate), 
					self.precision("base_paid_amount"))
					
		self.total_allocated_amount = abs(total_allocated_amount)
		self.base_total_allocated_amount = abs(base_total_allocated_amount)
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def set_unallocated_amount(self):
		self.unallocated_amount = 0;
		if self.party:
			party_amount = self.paid_amount if self.payment_type=="Receive" else self.received_amount
<<<<<<< HEAD

			if self.total_allocated_amount < party_amount:
				self.unallocated_amount = party_amount - self.total_allocated_amount

	def set_difference_amount(self):
		base_unallocated_amount = flt(self.unallocated_amount) * (flt(self.source_exchange_rate)
			if self.payment_type=="Receive" else flt(self.target_exchange_rate))

		base_party_amount = flt(self.base_total_allocated_amount) + flt(base_unallocated_amount)

=======
			
			total_deductions = sum([flt(d.amount) for d in self.get("deductions")])
			
			if self.total_allocated_amount < party_amount:
				if self.payment_type == "Receive":
					self.unallocated_amount = party_amount - (self.total_allocated_amount - total_deductions)
				else:
					self.unallocated_amount = party_amount - (self.total_allocated_amount + total_deductions)
				
	def set_difference_amount(self):
		base_unallocated_amount = flt(self.unallocated_amount) * (flt(self.source_exchange_rate) 
			if self.payment_type=="Receive" else flt(self.target_exchange_rate))
			
		base_party_amount = flt(self.base_total_allocated_amount) + flt(base_unallocated_amount)
		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		if self.payment_type == "Receive":
			self.difference_amount = base_party_amount - self.base_received_amount
		elif self.payment_type == "Pay":
			self.difference_amount = self.base_paid_amount - base_party_amount
		else:
			self.difference_amount = self.base_paid_amount - flt(self.base_received_amount)
<<<<<<< HEAD

		total_deductions = sum([flt(d.amount) for d in self.get("deductions")])

		self.difference_amount = flt(self.difference_amount - total_deductions,
			self.precision("difference_amount"))

	def clear_unallocated_reference_document_rows(self):
		self.set("references", self.get("references", {"allocated_amount": ["not in", [0, None, ""]]}))

		frappe.db.sql("""delete from `tabPayment Entry Reference`
			where parent = %s and allocated_amount = 0""", self.name)

	def validate_payment_against_negative_invoice(self):
		if ((self.payment_type=="Pay" and self.party_type=="Customer")
				or (self.payment_type=="Receive" and self.party_type=="Supplier")):

			total_negative_outstanding = sum([abs(flt(d.outstanding_amount))
				for d in self.get("references") if flt(d.outstanding_amount) < 0])

=======
			
		for d in self.get("deductions"):
			if d.amount:
				self.difference_amount -= flt(d.amount)
				
		self.difference_amount = flt(self.difference_amount, self.precision("difference_amount"))
				
	def clear_unallocated_reference_document_rows(self):
		self.set("references", self.get("references", {"allocated_amount": ["not in", [0, None, ""]]}))

		frappe.db.sql("""delete from `tabPayment Entry Reference` 
			where parent = %s and allocated_amount = 0""", self.name)
			
	def validate_payment_against_negative_invoice(self):
		if ((self.payment_type=="Pay" and self.party_type=="Customer") 
				or (self.payment_type=="Receive" and self.party_type=="Supplier")):
				
			total_negative_outstanding = sum([abs(flt(d.outstanding_amount)) 
				for d in self.get("references") if flt(d.outstanding_amount) < 0])
			
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			party_amount = self.paid_amount if self.payment_type=="Receive" else self.received_amount

			if not total_negative_outstanding:
				frappe.throw(_("Cannot {0} {1} {2} without any negative outstanding invoice")
<<<<<<< HEAD
					.format(self.payment_type, ("to" if self.party_type=="Customer" else "from"),
						self.party_type), InvalidPaymentEntry)

			elif party_amount > total_negative_outstanding:
				frappe.throw(_("Paid Amount cannot be greater than total negative outstanding amount {0}")
					.format(total_negative_outstanding), InvalidPaymentEntry)

=======
					.format(self.payment_type, ("to" if self.party_type=="Customer" else "from"), 
						self.party_type), InvalidPaymentEntry)
					
			elif party_amount > total_negative_outstanding:
				frappe.throw(_("Paid Amount cannot be greater than total negative outstanding amount {0}")
					.format(total_negative_outstanding), InvalidPaymentEntry)
			
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def set_title(self):
		if self.payment_type in ("Receive", "Pay"):
			self.title = self.party
		else:
			self.title = self.paid_from + " - " + self.paid_to
<<<<<<< HEAD

	def validate_transaction_reference(self):
		bank_account = self.paid_to if self.payment_type == "Receive" else self.paid_from
		bank_account_type = frappe.db.get_value("Account", bank_account, "account_type")

		if bank_account_type == "Bank":
			if not self.reference_no or not self.reference_date:
				frappe.throw(_("Reference No and Reference Date is mandatory for Bank transaction"))

	def set_remarks(self):
		if self.remarks: return

=======
			
	def validate_transaction_reference(self):
		bank_account = self.paid_to if self.payment_type == "Receive" else self.paid_from
		bank_account_type = frappe.db.get_value("Account", bank_account, "account_type")
		
		if bank_account_type == "Bank":
			if not self.reference_no or not self.reference_date:
				frappe.throw(_("Reference No and Reference Date is mandatory for Bank transaction"))
				
	def set_remarks(self):
		if self.remarks: return
		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		if self.payment_type=="Internal Transfer":
			remarks = [_("Amount {0} {1} transferred from {2} to {3}")
				.format(self.paid_from_account_currency, self.paid_amount, self.paid_from, self.paid_to)]
		else:
<<<<<<< HEAD

=======
			
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			remarks = [_("Amount {0} {1} {2} {3}").format(
				self.party_account_currency,
				self.paid_amount if self.payment_type=="Receive" else self.received_amount,
				_("received from") if self.payment_type=="Receive" else _("to"), self.party
			)]
<<<<<<< HEAD

=======
			
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		if self.reference_no:
			remarks.append(_("Transaction reference no {0} dated {1}")
				.format(self.reference_no, self.reference_date))

		if self.payment_type in ["Receive", "Pay"]:
			for d in self.get("references"):
				if d.allocated_amount:
<<<<<<< HEAD
					remarks.append(_("Amount {0} {1} against {2} {3}").format(self.party_account_currency,
						d.allocated_amount, d.reference_doctype, d.reference_name))

=======
					remarks.append(_("Amount {0} {1} against {2} {3}").format(self.party_account_currency, 
						d.allocated_amount, d.reference_doctype, d.reference_name))
		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		for d in self.get("deductions"):
			if d.amount:
				remarks.append(_("Amount {0} {1} deducted against {2}")
					.format(self.company_currency, d.amount, d.account))

		self.set("remarks", "\n".join(remarks))
<<<<<<< HEAD

	def make_gl_entries(self, cancel=0, adv_adj=0):
		if self.payment_type in ("Receive", "Pay") and not self.get("party_account_field"):
			self.setup_party_account_field()

=======
			
	def make_gl_entries(self, cancel=0, adv_adj=0):
		if self.payment_type in ("Receive", "Pay") and not self.get("party_account_field"):
			self.setup_party_account_field()
			
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		gl_entries = []
		self.add_party_gl_entries(gl_entries)
		self.add_bank_gl_entries(gl_entries)
		self.add_deductions_gl_entries(gl_entries)

		make_gl_entries(gl_entries, cancel=cancel, adv_adj=adv_adj)
<<<<<<< HEAD

=======
		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def add_party_gl_entries(self, gl_entries):
		if self.party_account:
			if self.payment_type=="Receive":
				against_account = self.paid_to
			else:
<<<<<<< HEAD
				against_account = self.paid_from


=======
				 against_account = self.paid_from
			
				
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			party_gl_dict = self.get_gl_dict({
				"account": self.party_account,
				"party_type": self.party_type,
				"party": self.party,
				"against": against_account,
				"account_currency": self.party_account_currency
			})
<<<<<<< HEAD

			dr_or_cr = "credit" if self.party_type in ["Customer", "Student"] else "debit"

=======
			
			dr_or_cr = "credit" if self.party_type == "Customer" else "debit"
			
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			for d in self.get("references"):
				gle = party_gl_dict.copy()
				gle.update({
					"against_voucher_type": d.reference_doctype,
					"against_voucher": d.reference_name
				})
<<<<<<< HEAD

				allocated_amount_in_company_currency = flt(flt(d.allocated_amount) * flt(d.exchange_rate),
					self.precision("paid_amount"))

=======
				
				allocated_amount_in_company_currency = flt(flt(d.allocated_amount) * flt(d.exchange_rate), 
					self.precision("paid_amount"))	
				
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				gle.update({
					dr_or_cr + "_in_account_currency": d.allocated_amount,
					dr_or_cr: allocated_amount_in_company_currency
				})
<<<<<<< HEAD

				gl_entries.append(gle)

			if self.unallocated_amount:
				base_unallocated_amount = base_unallocated_amount = self.unallocated_amount * \
					(self.source_exchange_rate if self.payment_type=="Receive" else self.target_exchange_rate)

				gle = party_gl_dict.copy()

=======
				
				gl_entries.append(gle)
				
			if self.unallocated_amount:
				base_unallocated_amount = base_unallocated_amount = self.unallocated_amount * \
					(self.source_exchange_rate if self.payment_type=="Receive" else self.target_exchange_rate)
					
				gle = party_gl_dict.copy()
				
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				gle.update({
					dr_or_cr + "_in_account_currency": self.unallocated_amount,
					dr_or_cr: base_unallocated_amount
				})

				gl_entries.append(gle)
<<<<<<< HEAD

=======
				
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def add_bank_gl_entries(self, gl_entries):
		if self.payment_type in ("Pay", "Internal Transfer"):
			gl_entries.append(
				self.get_gl_dict({
					"account": self.paid_from,
					"account_currency": self.paid_from_account_currency,
					"against": self.party if self.payment_type=="Pay" else self.paid_to,
					"credit_in_account_currency": self.paid_amount,
					"credit": self.base_paid_amount
				})
			)
		if self.payment_type in ("Receive", "Internal Transfer"):
			gl_entries.append(
				self.get_gl_dict({
					"account": self.paid_to,
					"account_currency": self.paid_to_account_currency,
					"against": self.party if self.payment_type=="Receive" else self.paid_from,
					"debit_in_account_currency": self.received_amount,
					"debit": self.base_received_amount
				})
			)
<<<<<<< HEAD

=======
			
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def add_deductions_gl_entries(self, gl_entries):
		for d in self.get("deductions"):
			if d.amount:
				account_currency = get_account_currency(d.account)
				if account_currency != self.company_currency:
					frappe.throw(_("Currency for {0} must be {1}").format(d.account, self.company_currency))
<<<<<<< HEAD

=======
					
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				gl_entries.append(
					self.get_gl_dict({
						"account": d.account,
						"account_currency": account_currency,
						"against": self.party or self.paid_from,
						"debit_in_account_currency": d.amount,
						"debit": d.amount,
						"cost_center": d.cost_center
					})
				)
<<<<<<< HEAD

=======
				
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def update_advance_paid(self):
		if self.payment_type in ("Receive", "Pay") and self.party:
			for d in self.get("references"):
				if d.allocated_amount and d.reference_doctype in ("Sales Order", "Purchase Order"):
					frappe.get_doc(d.reference_doctype, d.reference_name).set_total_advance_paid()

<<<<<<< HEAD
	def update_expense_claim(self):
		if self.payment_type =="Pay" and self.party:
			for d in self.get("references"):
				if d.reference_doctype=="Expense Claim" and d.reference_name:
					doc = frappe.get_doc("Expense Claim", d.reference_name)
					update_paid_amount(doc, self.paid_to)

	def on_recurring(self, reference_doc, subscription_doc):
		self.reference_no = reference_doc.name
		self.reference_date = nowdate()

@frappe.whitelist()
def get_outstanding_reference_documents(args):
	if isinstance(args, basestring):
		args = json.loads(args)

	party_account_currency = get_account_currency(args.get("party_account"))
	company_currency = frappe.db.get_value("Company", args.get("company"), "default_currency")

	# Get negative outstanding sales /purchase invoices
	total_field = "base_grand_total" if party_account_currency == company_currency else "grand_total"

	negative_outstanding_invoices = []
	if (args.get("party_type") != "Student"):
		negative_outstanding_invoices = get_negative_outstanding_invoices(args.get("party_type"),
			args.get("party"), args.get("party_account"), total_field)

	# Get positive outstanding sales /purchase invoices/ Fees
	outstanding_invoices = get_outstanding_invoices(args.get("party_type"), args.get("party"),
		args.get("party_account"))

	for d in outstanding_invoices:
		d["exchange_rate"] = 1
		if party_account_currency != company_currency:
			if d.voucher_type in ("Sales Invoice", "Purchase Invoice", "Expense Claim"):
				d["exchange_rate"] = frappe.db.get_value(d.voucher_type, d.voucher_no, "conversion_rate")
			elif d.voucher_type == "Journal Entry":
				d["exchange_rate"] = get_exchange_rate(
					party_account_currency,	company_currency, d.posting_date
				)
		if d.voucher_type in ("Purchase Invoice"):
			d["bill_no"] = frappe.db.get_value(d.voucher_type, d.voucher_no, "bill_no")

	# Get all SO / PO which are not fully billed or aginst which full advance not paid
	orders_to_be_billed = []
	if (args.get("party_type") != "Student"):
		orders_to_be_billed =  get_orders_to_be_billed(args.get("posting_date"),args.get("party_type"),
			args.get("party"), party_account_currency, company_currency)

	return negative_outstanding_invoices + outstanding_invoices + orders_to_be_billed

def get_orders_to_be_billed(posting_date, party_type, party, party_account_currency, company_currency):
	if party_type == "Customer":
		voucher_type = 'Sales Order'
	elif party_type == "Supplier":
		voucher_type = 'Purchase Order'
	elif party_type == "Employee":
		voucher_type = None

	orders = []
	if voucher_type:
		ref_field = "base_grand_total" if party_account_currency == company_currency else "grand_total"

		orders = frappe.db.sql("""
			select
				name as voucher_no,
				{ref_field} as invoice_amount,
				({ref_field} - advance_paid) as outstanding_amount,
				transaction_date as posting_date
			from
				`tab{voucher_type}`
			where
				{party_type} = %s
				and docstatus = 1
				and ifnull(status, "") != "Closed"
				and {ref_field} > advance_paid
				and abs(100 - per_billed) > 0.01
			order by
				transaction_date, name
			""".format(**{
				"ref_field": ref_field,
				"voucher_type": voucher_type,
				"party_type": scrub(party_type)
			}), party, as_dict = True)
=======
@frappe.whitelist()
def get_outstanding_reference_documents(args):
	args = json.loads(args)

	party_account_currency = get_account_currency(args.get("party_account"))
	company_currency = frappe.db.get_value("Company", args.get("company"), "default_currency")
	
	# Get negative outstanding sales /purchase invoices
	total_field = "base_grand_total" if party_account_currency == company_currency else "grand_total"
		
	negative_outstanding_invoices = get_negative_outstanding_invoices(args.get("party_type"), 
		args.get("party"), args.get("party_account"), total_field)

	# Get positive outstanding sales /purchase invoices
	outstanding_invoices = get_outstanding_invoices(args.get("party_type"), args.get("party"), 
		args.get("party_account"))
	
	for d in outstanding_invoices:
		d["exchange_rate"] = 1
		if party_account_currency != company_currency \
			and d.voucher_type in ("Sales Invoice", "Purchase Invoice"):
				d["exchange_rate"] = frappe.db.get_value(d.voucher_type, d.voucher_no, "conversion_rate")

	# Get all SO / PO which are not fully billed or aginst which full advance not paid
	orders_to_be_billed =  get_orders_to_be_billed(args.get("party_type"), args.get("party"), 
		party_account_currency, company_currency)
	
	return negative_outstanding_invoices + outstanding_invoices + orders_to_be_billed
	
def get_orders_to_be_billed(party_type, party, party_account_currency, company_currency):
	voucher_type = 'Sales Order' if party_type == "Customer" else 'Purchase Order'

	ref_field = "base_grand_total" if party_account_currency == company_currency else "grand_total"

	orders = frappe.db.sql("""
		select
			name as voucher_no,
			{ref_field} as invoice_amount,
			({ref_field} - advance_paid) as outstanding_amount,
			transaction_date as posting_date
		from
			`tab{voucher_type}`
		where
			{party_type} = %s
			and docstatus = 1
			and ifnull(status, "") != "Closed"
			and {ref_field} > advance_paid
			and abs(100 - per_billed) > 0.01
		order by
			transaction_date, name
		""".format(**{
			"ref_field": ref_field,
			"voucher_type": voucher_type,
			"party_type": scrub(party_type)
		}), party, as_dict = True)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	order_list = []
	for d in orders:
		d["voucher_type"] = voucher_type
<<<<<<< HEAD
		# This assumes that the exchange rate required is the one in the SO
		d["exchange_rate"] = get_exchange_rate(party_account_currency,
			company_currency, posting_date)
		order_list.append(d)

	return order_list

def get_negative_outstanding_invoices(party_type, party, party_account, total_field):
	if party_type != "Employee":
		voucher_type = "Sales Invoice" if party_type == "Customer" else "Purchase Invoice"
		return frappe.db.sql("""
			select
				"{voucher_type}" as voucher_type, name as voucher_no,
				{total_field} as invoice_amount, outstanding_amount, posting_date,
				due_date, conversion_rate as exchange_rate
			from
				`tab{voucher_type}`
			where
				{party_type} = %s and {party_account} = %s and docstatus = 1 and outstanding_amount < 0
			order by
				posting_date, name
			""".format(**{
				"total_field": total_field,
				"voucher_type": voucher_type,
				"party_type": scrub(party_type),
				"party_account": "debit_to" if party_type=="Customer" else "credit_to"
			}), (party, party_account), as_dict = True)
	else:
		return []

=======
		d["exchange_rate"] = get_exchange_rate(party_account_currency, company_currency)
		order_list.append(d)

	return order_list
	
def get_negative_outstanding_invoices(party_type, party, party_account, total_field):
	voucher_type = "Sales Invoice" if party_type == "Customer" else "Purchase Invoice"
	return frappe.db.sql("""
		select
			"{voucher_type}" as voucher_type, name as voucher_no, 
			{total_field} as invoice_amount, outstanding_amount, posting_date, 
			due_date, conversion_rate as exchange_rate
		from
			`tab{voucher_type}`
		where
			{party_type} = %s and {party_account} = %s and docstatus = 1 and outstanding_amount < 0
		order by
			posting_date, name
		""".format(**{
			"total_field": total_field,
			"voucher_type": voucher_type,
			"party_type": scrub(party_type),
			"party_account": "debit_to" if party_type=="Customer" else "credit_to"
		}), (party, party_account), as_dict = True)
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
@frappe.whitelist()
def get_party_details(company, party_type, party, date):
	if not frappe.db.exists(party_type, party):
		frappe.throw(_("Invalid {0}: {1}").format(party_type, party))
<<<<<<< HEAD

	party_account = get_party_account(party_type, party, company)

	account_currency = get_account_currency(party_account)
	account_balance = get_balance_on(party_account, date)
	party_balance = get_balance_on(party_type=party_type, party=party)

=======
		
	party_account = get_party_account(party_type, party, company)
	
	account_currency = get_account_currency(party_account)
	account_balance = get_balance_on(party_account, date)
	party_balance = get_balance_on(party_type=party_type, party=party)
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	return {
		"party_account": party_account,
		"party_account_currency": account_currency,
		"party_balance": party_balance,
		"account_balance": account_balance
	}

<<<<<<< HEAD
@frappe.whitelist()
=======
@frappe.whitelist()	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
def get_account_details(account, date):
	frappe.has_permission('Payment Entry', throw=True)
	return frappe._dict({
		"account_currency": get_account_currency(account),
		"account_balance": get_balance_on(account, date),
		"account_type": frappe.db.get_value("Account", account, "account_type")
	})
<<<<<<< HEAD

=======
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
@frappe.whitelist()
def get_company_defaults(company):
	fields = ["write_off_account", "exchange_gain_loss_account", "cost_center"]
	ret = frappe.db.get_value("Company", company, fields, as_dict=1)
<<<<<<< HEAD

=======
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	for fieldname in fields:
		if not ret[fieldname]:
			frappe.throw(_("Please set default {0} in Company {1}")
				.format(frappe.get_meta("Company").get_label(fieldname), company))
<<<<<<< HEAD

=======
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	return ret

@frappe.whitelist()
def get_reference_details(reference_doctype, reference_name, party_account_currency):
	total_amount = outstanding_amount = exchange_rate = None
	ref_doc = frappe.get_doc(reference_doctype, reference_name)
<<<<<<< HEAD

	if reference_doctype == "Fees":
		total_amount = ref_doc.get("grand_total")
		exchange_rate = 1
		outstanding_amount = ref_doc.get("outstanding_amount")
	elif reference_doctype != "Journal Entry":
		if party_account_currency == ref_doc.company_currency:
			if ref_doc.doctype == "Expense Claim":
				total_amount = ref_doc.total_sanctioned_amount
			else:
				total_amount = ref_doc.base_grand_total
			exchange_rate = 1
		else:
			total_amount = ref_doc.grand_total

			# Get the exchange rate from the original ref doc
			# or get it based on the posting date of the ref doc
			exchange_rate = ref_doc.get("conversion_rate") or \
				get_exchange_rate(party_account_currency, ref_doc.company_currency, ref_doc.posting_date)

		outstanding_amount = ref_doc.get("outstanding_amount") \
			if reference_doctype in ("Sales Invoice", "Purchase Invoice", "Expense Claim") \
			else flt(total_amount) - flt(ref_doc.advance_paid)
	else:
		# Get the exchange rate based on the posting date of the ref doc
		exchange_rate = get_exchange_rate(party_account_currency,
			ref_doc.company_currency, ref_doc.posting_date)

=======
	
	if reference_doctype != "Journal Entry":
		if party_account_currency == ref_doc.company_currency:
			total_amount = ref_doc.base_grand_total
			exchange_rate = 1
		else:
			total_amount = ref_doc.grand_total
			exchange_rate = ref_doc.get("conversion_rate") or \
				get_exchange_rate(party_account_currency, ref_doc.company_currency)
		
		outstanding_amount = ref_doc.get("outstanding_amount") \
			if reference_doctype in ("Sales Invoice", "Purchase Invoice") \
			else flt(total_amount) - flt(ref_doc.advance_paid)			
	else:
		exchange_rate = get_exchange_rate(party_account_currency, ref_doc.company_currency)
		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	return frappe._dict({
		"due_date": ref_doc.get("due_date"),
		"total_amount": total_amount,
		"outstanding_amount": outstanding_amount,
		"exchange_rate": exchange_rate
	})
<<<<<<< HEAD

@frappe.whitelist()
def get_payment_entry(dt, dn, party_amount=None, bank_account=None, bank_amount=None):
	doc = frappe.get_doc(dt, dn)

	if dt in ("Sales Order", "Purchase Order") and flt(doc.per_billed, 2) > 0:
		frappe.throw(_("Can only make payment against unbilled {0}").format(dt))

	if dt in ("Sales Invoice", "Sales Order"):
		party_type = "Customer"
	elif dt in ("Purchase Invoice", "Purchase Order"):
		party_type = "Supplier"
	elif dt in ("Expense Claim"):
		party_type = "Employee"
	elif dt in ("Fees"):
		party_type = "Student"
=======
	
@frappe.whitelist()
def get_payment_entry(dt, dn, party_amount=None, bank_account=None, bank_amount=None):
	doc = frappe.get_doc(dt, dn)
	
	if dt in ("Sales Order", "Purchase Order") and flt(doc.per_billed, 2) > 0:
		frappe.throw(_("Can only make payment against unbilled {0}").format(dt))
	
	party_type = "Customer" if dt in ("Sales Invoice", "Sales Order") else "Supplier"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	# party account
	if dt == "Sales Invoice":
		party_account = doc.debit_to
	elif dt == "Purchase Invoice":
		party_account = doc.credit_to
<<<<<<< HEAD
	elif dt == "Expense Claim":
		party_account = doc.payable_account if doc.docstatus==1 else doc.advance_account
	elif dt == "Fees":
		party_account = doc.receivable_account
	else:
		party_account = get_party_account(party_type, doc.get(party_type.lower()), doc.company)

	party_account_currency = doc.get("party_account_currency") or get_account_currency(party_account)

	# payment type
	if (dt == "Sales Order" or (dt in ("Sales Invoice", "Fees") and doc.outstanding_amount > 0)) \
=======
	else:
		party_account = get_party_account(party_type, doc.get(party_type.lower()), doc.company)
		
	party_account_currency = doc.get("party_account_currency") or get_account_currency(party_account)
	
	# payment type
	if (dt == "Sales Order" or (dt=="Sales Invoice" and doc.outstanding_amount > 0)) \
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		or (dt=="Purchase Invoice" and doc.outstanding_amount < 0):
			payment_type = "Receive"
	else:
		payment_type = "Pay"
<<<<<<< HEAD

=======
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	# amounts
	grand_total = outstanding_amount = 0
	if party_amount:
		grand_total = outstanding_amount = party_amount
	elif dt in ("Sales Invoice", "Purchase Invoice"):
<<<<<<< HEAD
		grand_total = doc.base_grand_total \
			if party_account_currency == doc.company_currency else doc.grand_total
		outstanding_amount = doc.outstanding_amount
	elif dt in ("Expense Claim"):
		grand_total = doc.total_sanctioned_amount
		outstanding_amount = flt(doc.total_sanctioned_amount) - flt(doc.total_amount_reimbursed) \
			- flt(doc.total_advance_paid)
	elif dt == "Fees":
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		grand_total = doc.grand_total
		outstanding_amount = doc.outstanding_amount
	else:
		total_field = "base_grand_total" if party_account_currency == doc.company_currency else "grand_total"
		grand_total = flt(doc.get(total_field))
		outstanding_amount = grand_total - flt(doc.advance_paid)

	# bank or cash
<<<<<<< HEAD
	bank = get_default_bank_cash_account(doc.company, "Bank", mode_of_payment=doc.get("mode_of_payment"),
		account=bank_account)

=======
	bank = get_default_bank_cash_account(doc.company, "Bank", mode_of_payment=doc.get("mode_of_payment"), 
		account=bank_account)
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	paid_amount = received_amount = 0
	if party_account_currency == bank.account_currency:
		paid_amount = received_amount = abs(outstanding_amount)
	elif payment_type == "Receive":
		paid_amount = abs(outstanding_amount)
		if bank_amount:
			received_amount = bank_amount
	else:
		received_amount = abs(outstanding_amount)
		if bank_amount:
			paid_amount = bank_amount
<<<<<<< HEAD

=======
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	pe = frappe.new_doc("Payment Entry")
	pe.payment_type = payment_type
	pe.company = doc.company
	pe.posting_date = nowdate()
	pe.mode_of_payment = doc.get("mode_of_payment")
	pe.party_type = party_type
	pe.party = doc.get(scrub(party_type))
	pe.paid_from = party_account if payment_type=="Receive" else bank.account
	pe.paid_to = party_account if payment_type=="Pay" else bank.account
	pe.paid_from_account_currency = party_account_currency \
		if payment_type=="Receive" else bank.account_currency
	pe.paid_to_account_currency = party_account_currency if payment_type=="Pay" else bank.account_currency
	pe.paid_amount = paid_amount
	pe.received_amount = received_amount
	pe.allocate_payment_amount = 1
<<<<<<< HEAD
	pe.letter_head = doc.get("letter_head")

=======
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	pe.append("references", {
		"reference_doctype": dt,
		"reference_name": dn,
		"due_date": doc.get("due_date"),
		"total_amount": grand_total,
		"outstanding_amount": outstanding_amount,
		"allocated_amount": outstanding_amount
	})

	pe.setup_party_account_field()
	pe.set_missing_values()
	if party_account and bank:
		pe.set_exchange_rate()
		pe.set_amounts()
	return pe