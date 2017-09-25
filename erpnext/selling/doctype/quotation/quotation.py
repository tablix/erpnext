# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.mapper import get_mapped_doc
<<<<<<< HEAD
from frappe.utils import flt, nowdate, getdate
from frappe import _
=======
from frappe import _, msgprint
from frappe.utils import money_in_words
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

from erpnext.controllers.selling_controller import SellingController

form_grid_templates = {
	"items": "templates/form_grid/item_grid.html"
}

class Quotation(SellingController):
<<<<<<< HEAD
	def set_indicator(self):
		if self.docstatus==1:
			self.indicator_color = 'blue'
			self.indicator_title = 'Submitted'
		if self.valid_till and getdate(self.valid_till) < getdate(nowdate()):
			self.indicator_color = 'darkgrey'
			self.indicator_title = 'Expired'

	def validate(self):
		super(Quotation, self).validate()
		self.set_status()
		self.update_opportunity()
		self.validate_order_type()
		self.validate_uom_is_integer("stock_uom", "qty")
		self.validate_quotation_to()
		self.validate_valid_till()
		if self.items:
			self.with_items = 1

	def validate_valid_till(self):
		if self.valid_till and self.valid_till < self.transaction_date:
			frappe.throw(_("Valid till date cannot be before transaction date"))

=======
	def validate(self):
		super(Quotation, self).validate()
		self.set_status()
		self.validate_order_type()
		#self.validate_uom_is_integer("stock_uom", "qty")
		#new addition
		#if self.is_amc:
		#	self.validate_total()
		self.validate_quotation_to()
		if ((self.is_proposal) or (self.technical_proposal) or (self.is_amc)):
			self.validate_proposal_index()
		else:
			to_remove = []
			for d in self.get("terms_checklist"):
				to_remove.append(d)
			[self.remove(d) for d in to_remove]
			
			self.append("terms_checklist", {"terms": "Scope of Work" , "check": 1})
			self.append("terms_checklist", {"terms": "Price", "check": 1})
			self.append("terms_checklist", {"terms": "Validity", "check": 1})
			self.append("terms_checklist", {"terms": "Certification", "check": 1})
			self.append("terms_checklist", {"terms": "Payment Terms", "check": 1})
			self.append("terms_checklist", {"terms": "Mobilization Period", "check": 1})
			self.append("terms_checklist", {"terms": "Material Delivery Period", "check": 1})
			self.append("terms_checklist", {"terms": "Completion Period", "check": 1})
			self.append("terms_checklist", {"terms": "Delivery Location", "check": 1})
			self.append("terms_checklist", {"terms": "Title and Risk", "check": 1})
			self.append("terms_checklist", {"terms": "Incoterm", "check": 1})
			self.append("terms_checklist", {"terms": "Warranty", "check": 1})
			self.append("terms_checklist", {"terms": "Ownership of the Software and documentation", "check": 1})
			self.append("terms_checklist", {"terms": "Other Conditions", "check": 1})
			self.append("terms_checklist", {"terms": "Inclusions", "check": 1})
			self.append("terms_checklist", {"terms": "Exclusions", "check": 1})
		#adding boq & opp ref
		for item in self.get('items'):
			#item.boq_ref = self.boq
			item.opp_ref = self.opportunity
			if item.uom == "" or item.uom is None:
				item.uom = item.stock_uom
			
		#validating extra charges
		if self.vat > 0 or self.duties > 0 or self.other_charges > 0:
			self.validate_other_charges()
		
		self.set_boq_status()
		#adding attched docs
		#if self.name:
		#	attached_docs_details = frappe.db.sql("UPDATE `tabFile` SET attached_to_name = %s and attached_to_doctype = 'Quotation' WHERE attached_to_name = %s", (self.name, self.boq))
		
		if self.items:	
			self.with_items = 1
			

		

	#new addition	
	
	def validate_total_currency(self):
		conversion_rate = frappe.db.get_value('Currency Exchange', {"from_currency":"AED","to_currency":self.change_currency_to}, 'exchange_rate')
		self.grand_total_new_currency = self.grand_total * conversion_rate
		self.in_words_new_currency = money_in_words(self.grand_total_new_currency, self.change_currency_to)
	
	def validate_other_charges(self):
		self.net_total = self.net_total + self.vat + self.duties + self.other_charges
		self.base_net_total = self.base_net_total + self.vat + self.duties + self.other_charges
		self.grand_total = self.grand_total + self.vat + self.duties + self.other_charges
		self.base_grand_total = self.base_grand_total + self.vat + self.duties + self.other_charges
	
	def validate_total(self):
		for item in self.get("items"):
			item.rate = 0.00
			item.amount = 0.00
		self.total = self.total_cost
		self.base_total = self.total * self.conversion_rate
		if self.additional_discount_percentage:
			self.discount_amount = (self.total * self.additional_discount_percentage)/100
			if self.currency != "AED":
				self.base_discount_amount = self.discount_amount * self.conversion_rate
		if self.discount_amount > 0.00:
			self.grand_total = self.total - self.discount_amount
			self.net_total = self.grand_total
		else:
			self.grand_total = self.total
			self.net_total = self.total
		self.in_words = money_in_words(self.grand_total, self.currency)	
		
		if self.currency != "AED":
			self.base_grand_total = self.grand_total * self.conversion_rate
			self.base_in_words = money_in_words(self.base_grand_total)
			self.base_rounded_total = self.base_grand_total
			self.base_net_total = self.base_grand_total
		
		 
	
	
	def validate_proposal_index(self):
	
		if not self.get('appendix'):
			if ((self.is_proposal) or (self.technical_proposal)):
				self.append("appendix", {"topic": "Schematic Drawings", "check": 0})
				self.append("appendix", {"topic": "Executive Summary", "check": 0})
				self.append("appendix", {"topic": "Signed & Stamped copy of " + str(self.customer) + " Standard Terms & Conditions- Acceptance", "check": 0})
				self.append("appendix", {"topic": "RFT Compliance Statement", "check": 0})
				self.append("appendix", {"topic": "Copy of RFT signed & stamped", "check": 0})
				
		if not self.get('technical_quotation_index'):
			if self.technical_proposal:
				self.append("technical_quotation_index", {"topic": "Statement of Confidentiality & Non-Disclosure", "page_number": 3})
				self.append("technical_quotation_index", {"topic": "Executive Summary", "page_number": 4})
				self.append("technical_quotation_index", {"topic": "1.Company Background", "page_number": 5})
				self.append("technical_quotation_index", {"topic": "2. Identification of Needs", "page_number": 8})
				self.append("technical_quotation_index", {"topic": "2.1. " + str(self.solution) + " for " + str(self.customer) + " Requirements", "page_number": 8})
				self.append("technical_quotation_index", {"topic": "2.2. Needs Identification", "page_number": 9})
				self.append("technical_quotation_index", {"topic": "2.3. Project Scope", "page_number": 9})
				self.append("technical_quotation_index", {"topic": "3. Proposed Solution", "page_number": 10})
				self.append("technical_quotation_index", {"topic": "3.1. Objectives", "page_number": 10})
				self.append("technical_quotation_index", {"topic": "3.2. Solution", "page_number": 10})
				self.append("technical_quotation_index", {"topic": "3.2.1. Deliverables", "page_number": 10})
				self.append("technical_quotation_index", {"topic": "3.2.2. Requirements vs Solution", "page_number": 10})
				self.append("technical_quotation_index", {"topic": "3.2.3. System Overview", "page_number": 11})
				self.append("technical_quotation_index", {"topic": "3.2.3.1. Product Overview", "page_number": 11})
				self.append("technical_quotation_index", {"topic": "3.2.3.2. Site Overview", "page_number": 12})
				self.append("technical_quotation_index", {"topic": "3.2.4. " + str(self.customer)+ " - " + str(self.solution) + " Project Team", "page_number": 12})
				self.append("technical_quotation_index", {"topic": "4. Why Choose Tablix?", "page_number": 13})
				self.append("technical_quotation_index", {"topic": "4.1. Benefits of Our Proposed Plan", "page_number": 13})
				self.append("technical_quotation_index", {"topic": "4.2. Competitive Advantages", "page_number": 13})
				self.append("technical_quotation_index", {"topic": "4.3. Team Qualifications", "page_number": 14})
				self.append("technical_quotation_index", {"topic": "4.4. Success Stories", "page_number": 15})
				self.append("technical_quotation_index", {"topic": "5. Implementation Plan", "page_number": 16})
				self.append("technical_quotation_index", {"topic": "5.1. Methodology", "page_number": 16})
				self.append("technical_quotation_index", {"topic": "5.2. Project Schedule", "page_number": 16})
				self.append("technical_quotation_index", {"topic": "5.3. Testing & Evaluation", "page_number": 16})
				self.append("technical_quotation_index", {"topic": "5.3.1. Performance metrics", "page_number": 16})
				self.append("technical_quotation_index", {"topic": "6. Bill of Quantities", "page_number": 17})
				self.append("technical_quotation_index", {"topic": "6.1. BoQ", "page_number": 17})
				self.append("technical_quotation_index", {"topic": "6.2. Notes", "page_number": 19})
				self.append("technical_quotation_index", {"topic": "6.3. Terms & Conditions", "page_number": 19})		
				self.append("technical_quotation_index", {"topic": "7. Conclusion", "page_number": 23})
				self.append("technical_quotation_index", {"topic": "8. PROPOSAL ACCEPTANCE", "page_number": 24})
				self.append("technical_quotation_index", {"topic": "Appendix A", "page_number": 25})
				self.append("technical_quotation_index", {"topic": "Appendix B", "page_number": 26})
				self.append("technical_quotation_index", {"topic": "Appendix C", "page_number": 27})
				self.append("technical_quotation_index", {"topic": "Appendix D", "page_number": 28})
			
			
				
		
		if not self.get('quotation_index'):
			if ((self.is_proposal == 1 and self.is_boq == 1 and self.is_amc == 0) or (self.is_proposal == 1 and self.is_boq == 1 and self.is_amc == 1)):
				self.append("quotation_index", {"topic": "Statement of Confidentiality & Non-Disclosure", "page_number": 3})
				self.append("quotation_index", {"topic": "Executive Summary", "page_number": 4})
				self.append("quotation_index", {"topic": "1.Company Background", "page_number": 5})
				self.append("quotation_index", {"topic": "2. Identification of Needs", "page_number": 8})
				self.append("quotation_index", {"topic": "2.1. " + str(self.solution) + " for " + str(self.customer) + " Requirements", "page_number": 8})
				self.append("quotation_index", {"topic": "2.2. Needs Identification", "page_number": 9})
				self.append("quotation_index", {"topic": "2.3. Project Scope", "page_number": 9})
				self.append("quotation_index", {"topic": "3. Proposed Solution", "page_number": 10})
				self.append("quotation_index", {"topic": "3.1. Objectives", "page_number": 10})
				self.append("quotation_index", {"topic": "3.2. Solution", "page_number": 10})
				self.append("quotation_index", {"topic": "3.2.1. Deliverables", "page_number": 10})
				self.append("quotation_index", {"topic": "3.2.2. Requirements vs Solution", "page_number": 10})
				self.append("quotation_index", {"topic": "3.2.3. System Overview", "page_number": 11})
				self.append("quotation_index", {"topic": "3.2.3.1. Product Overview", "page_number": 11})
				self.append("quotation_index", {"topic": "3.2.3.2. Site Overview", "page_number": 12})
				self.append("quotation_index", {"topic": "3.2.4. " + str(self.customer)+ " - " + str(self.solution) + " Project Team", "page_number": 12})
				self.append("quotation_index", {"topic": "4. Why Choose Tablix?", "page_number": 13})
				self.append("quotation_index", {"topic": "4.1. Benefits of Our Proposed Plan", "page_number": 13})
				self.append("quotation_index", {"topic": "4.2. Competitive Advantages", "page_number": 13})
				self.append("quotation_index", {"topic": "4.3. Team Qualifications", "page_number": 14})
				self.append("quotation_index", {"topic": "4.4. Success Stories", "page_number": 15})
				self.append("quotation_index", {"topic": "5. Implementation Plan", "page_number": 16})
				self.append("quotation_index", {"topic": "5.1. Methodology", "page_number": 16})
				self.append("quotation_index", {"topic": "5.2. Project Schedule", "page_number": 16})
				self.append("quotation_index", {"topic": "5.3. Testing & Evaluation", "page_number": 16})
				self.append("quotation_index", {"topic": "5.3.1. Performance metrics", "page_number": 16})
				self.append("quotation_index", {"topic": "6. Costs", "page_number": 17})
				self.append("quotation_index", {"topic": "6.1. Cost Breakdown", "page_number": 17})
				self.append("quotation_index", {"topic": "6.2. Notes", "page_number": 19})
				self.append("quotation_index", {"topic": "6.3. Terms & Conditions", "page_number": 19})		
				self.append("quotation_index", {"topic": "7. Conclusion", "page_number": 23})
				self.append("quotation_index", {"topic": "8. PROPOSAL ACCEPTANCE", "page_number": 24})
				self.append("quotation_index", {"topic": "Appendix A", "page_number": 25})
				self.append("quotation_index", {"topic": "Appendix B", "page_number": 26})
				self.append("quotation_index", {"topic": "Appendix C", "page_number": 27})
				self.append("quotation_index", {"topic": "Appendix D", "page_number": 28})
			if (self.is_boq == 0 and self.is_amc == 1 and self.is_proposal == 1):
				self.append("quotation_index", {"topic": "INTRODUCTION", "page_number": 3})
				self.append("quotation_index", {"topic": "1. SOLUTION DESCRIPTION", "page_number": 4})
				self.append("quotation_index", {"topic": "1.1. Requirement", "page_number": 4})
				self.append("quotation_index", {"topic": "1.1.1. Annexure A", "page_number": 4})
				self.append("quotation_index", {"topic": "1.2. The Solution", "page_number": 5})
				self.append("quotation_index", {"topic": "1.2.1. Annexure B", "page_number": 5})
				self.append("quotation_index", {"topic": "2. PRICING TERMS", "page_number": 6})
				self.append("quotation_index", {"topic": "2.1. Terms and Conditions", "page_number": 6})
				self.append("quotation_index", {"topic": "2.2. Pricing Summary", "page_number": 6})
				self.append("quotation_index", {"topic": "2.3. Service Level Agreement", "page_number": 7})
				self.append("quotation_index", {"topic": "3. PRICE INCLUSIONS & EXCLUSIONS", "page_number": 8})
				self.append("quotation_index", {"topic": "3.1. Solution Inclusions", "page_number": 8})
				self.append("quotation_index", {"topic": "3.2. Solution Exclusions", "page_number": 8})
				self.append("quotation_index", {"topic": "4. PROPOSAL ACCEPTANCE", "page_number": 8})
				
			if (self.is_boq == 0 and self.is_amc == 1 and self.technical_proposal == 1):
				self.append("quotation_index", {"topic": "INTRODUCTION", "page_number": 3})
				self.append("quotation_index", {"topic": "1. SOLUTION DESCRIPTION", "page_number": 4})
				self.append("quotation_index", {"topic": "1.1. Requirement", "page_number": 4})
				self.append("quotation_index", {"topic": "1.1.1. Annexure A", "page_number": 4})
				self.append("quotation_index", {"topic": "1.2. The Solution", "page_number": 5})
				self.append("quotation_index", {"topic": "1.2.1. Annexure B", "page_number": 5})
				self.append("quotation_index", {"topic": "2. AMC TERMS", "page_number": 6})
				self.append("quotation_index", {"topic": "2.1. Terms and Conditions", "page_number": 6})
				#self.append("quotation_index", {"topic": "2.2. Pricing Summary", "page_number": 6})
				self.append("quotation_index", {"topic": "2.2. Service Level Agreement", "page_number": 7})
				self.append("quotation_index", {"topic": "3. SOLUTION INCLUSIONS & EXCLUSIONS", "page_number": 8})
				self.append("quotation_index", {"topic": "3.1. Solution Inclusions", "page_number": 8})
				self.append("quotation_index", {"topic": "3.2. Solution Exclusions", "page_number": 8})
				self.append("quotation_index", {"topic": "4. PROPOSAL ACCEPTANCE", "page_number": 8})
				

	
	def set_boq_status(self):
		frappe.db.set_value("Boq", self.boq, "status", "Quotation")
		frappe.db.set_value("Boq", self.boq, "temp_status", "Quotation")
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def has_sales_order(self):
		return frappe.db.get_value("Sales Order Item", {"prevdoc_docname": self.name, "docstatus": 1})

	def validate_order_type(self):
		super(Quotation, self).validate_order_type()

	def validate_quotation_to(self):
		if self.customer:
			self.quotation_to = "Customer"
			self.lead = None
		elif self.lead:
			self.quotation_to = "Lead"
<<<<<<< HEAD

	def update_lead(self):
		if self.lead:
			frappe.get_doc("Lead", self.lead).set_status(update=True)
=======
			lead_details = frappe.db.sql("select company_name from `tabLead` where name = %s", self.lead)
			lead_name = lead_details[0][0]
			self.lead_name = lead_name
			self.customer_name = lead_name
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	def update_opportunity(self):
		for opportunity in list(set([d.prevdoc_docname for d in self.get("items")])):
			if opportunity:
<<<<<<< HEAD
				self.update_opportunity_status(opportunity)

		if self.opportunity:
			self.update_opportunity_status()

	def update_opportunity_status(self, opportunity=None):
		if not opportunity:
			opportunity = self.opportunity

		opp = frappe.get_doc("Opportunity", opportunity)
		opp.status = None
		opp.set_status(update=True)
=======
				frappe.get_doc("Opportunity", opportunity).set_status(update=True)
		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	def declare_order_lost(self, arg):
		if not self.has_sales_order():
			frappe.db.set(self, 'status', 'Lost')
			frappe.db.set(self, 'order_lost_reason', arg)
			self.update_opportunity()
<<<<<<< HEAD
			self.update_lead()
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		else:
			frappe.throw(_("Cannot set as Lost as Sales Order is made."))

	def check_item_table(self):
		if not self.get('items'):
			frappe.throw(_("Please enter item details"))

	def on_submit(self):
<<<<<<< HEAD
		self.check_item_table()
=======
		#self.check_item_table()
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

		# Check for Approving Authority
		frappe.get_doc('Authorization Control').validate_approving_authority(self.doctype, self.company, self.base_grand_total, self)

		#update enquiry status
		self.update_opportunity()
<<<<<<< HEAD
		self.update_lead()
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	def on_cancel(self):
		#update enquiry status
		self.set_status(update=True)
		self.update_opportunity()
<<<<<<< HEAD
		self.update_lead()
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	def print_other_charges(self,docname):
		print_lst = []
		for d in self.get('taxes'):
			lst1 = []
			lst1.append(d.description)
			lst1.append(d.total)
			print_lst.append(lst1)
		return print_lst

<<<<<<< HEAD
	def on_recurring(self, reference_doc, subscription_doc):
		self.valid_till = None

def get_list_context(context=None):
	from erpnext.controllers.website_list_for_contact import get_list_context
	list_context = get_list_context(context)
	list_context.update({
		'show_sidebar': True,
		'show_search': True,
		'no_breadcrumbs': True,
		'title': _('Quotations'),
	})

	return list_context

@frappe.whitelist()
def make_sales_order(source_name, target_doc=None):
	quotation = frappe.db.get_value("Quotation", source_name, ["transaction_date", "valid_till"], as_dict = 1)
	if quotation.valid_till and (quotation.valid_till < quotation.transaction_date or quotation.valid_till < getdate(nowdate())):
		frappe.throw(_("Validity period of this quotation has ended."))
=======

@frappe.whitelist()
def make_sales_order(source_name, target_doc=None):
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	return _make_sales_order(source_name, target_doc)

def _make_sales_order(source_name, target_doc=None, ignore_permissions=False):
	customer = _make_customer(source_name, ignore_permissions)

	def set_missing_values(source, target):
		if customer:
			target.customer = customer.name
			target.customer_name = customer.customer_name
		target.ignore_pricing_rule = 1
		target.flags.ignore_permissions = ignore_permissions
		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")

<<<<<<< HEAD
	def update_item(obj, target, source_parent):
		target.stock_qty = flt(obj.qty) * flt(obj.conversion_factor)

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	doclist = get_mapped_doc("Quotation", source_name, {
			"Quotation": {
				"doctype": "Sales Order",
				"validation": {
					"docstatus": ["=", 1]
				}
			},
			"Quotation Item": {
				"doctype": "Sales Order Item",
				"field_map": {
					"parent": "prevdoc_docname"
<<<<<<< HEAD
				},
				"postprocess": update_item
=======
				}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			},
			"Sales Taxes and Charges": {
				"doctype": "Sales Taxes and Charges",
				"add_if_empty": True
			},
			"Sales Team": {
				"doctype": "Sales Team",
				"add_if_empty": True
			}
		}, target_doc, set_missing_values, ignore_permissions=ignore_permissions)

	# postprocess: fetch shipping address, set missing values

	return doclist

def _make_customer(source_name, ignore_permissions=False):
	quotation = frappe.db.get_value("Quotation", source_name, ["lead", "order_type", "customer"])
	if quotation and quotation[0] and not quotation[2]:
		lead_name = quotation[0]
		customer_name = frappe.db.get_value("Customer", {"lead_name": lead_name},
			["name", "customer_name"], as_dict=True)
		if not customer_name:
			from erpnext.crm.doctype.lead.lead import _make_customer
			customer_doclist = _make_customer(lead_name, ignore_permissions=ignore_permissions)
			customer = frappe.get_doc(customer_doclist)
			customer.flags.ignore_permissions = ignore_permissions
			if quotation[1] == "Shopping Cart":
				customer.customer_group = frappe.db.get_value("Shopping Cart Settings", None,
					"default_customer_group")

			try:
				customer.insert()
				return customer
			except frappe.NameError:
				if frappe.defaults.get_global_default('cust_master_name') == "Customer Name":
					customer.run_method("autoname")
					customer.name += "-" + lead_name
					customer.insert()
					return customer
				else:
					raise
			except frappe.MandatoryError:
				frappe.local.message_log = []
				frappe.throw(_("Please create Customer from Lead {0}").format(lead_name))
		else:
			return customer_name
