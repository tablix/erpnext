# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, flt, round_based_on_smallest_currency_fraction, get_link_to_form, money_in_words
from frappe.desk.form import assign_to
from erpnext.accounts.party import get_party_account_currency
import datetime


form_grid_templates = {
	"items": "templates/form_grid/boq_grid.html"
}

sales_coordinator_rep = "remriz.estella@tablix.ae"
cto = "bala@tablix.ae"
DE_rep = "lathesh@tablix.ae"
cbdo = "kartik@tablix.ae"
finance_emp = "bhavish@tablix.ae"
commercial_mgmr = "ali@tablix.ae"


class Boq(Document):
	def validate(self):
		#self.item_total()
		if self.status == "Designing":
			if self.technical_docs or self.compliance_statement:
				if not frappe.db.sql("select name from `tabFile` where attached_to_name = %s", self.name):
					frappe.throw(_("No documents attached"))
		if self.status == "Costing":
			if self.compliance_statements:
				if not frappe.db.sql("select name from `tabFile` where attached_to_name = %s", self.name):
					frappe.throw(_("No documents attached"))
		self.temp_status = self.status
		
		if self.prev_status == 'Cancel':
			self.status = 'Sales Margin'
		self.prev_status = ''
		
		#new addition	
		if self.comprehensive:
			self.amc_type = "Comprehensive"
		if self.non_comprehensive:
			self.amc_type = "Non Comprehensive"
			
		if self.discount_amt:
			if self.percentage == 0 and self.value == 0:
				frappe.throw(_("Discount Type not selected. Kindly select 'Percentage'or 'Value'!!!!!"))
				
		if self.boq :
			self.proposed_project_completion_time_ = self.proposed_project_completion_time + self.material_delivery_period
		
		if self.is_amc:
			self.validate_checklist()
		if self.boq:
			self.validate_terms_checklist()
			self.validate_deliverables()

		#validate mandatory fields
		self.validate_proposal()
			
		if self.status == "Boq Complete" :
			self.validate_payment_terms_total()
			
		for data in self.get('payment_term_table'):
			data.opp_ref = self.opportunity
		
		to_remove = []
		for d in self.get("site_costing"):
			to_remove.append(d)
		[self.remove(d) for d in to_remove]
		
		self.total()
			
			
	def item_total(self):
		for item in self.get("items"):
			item.cost_amount = flt(item.current_cost * item.qty)
			margin = flt(item.margin_percent) / 100
			margin = flt(1- margin)
			item.selling_price = flt(item.current_cost) / margin
			num_dec = str(flt(item.selling_price) - int(item.selling_price))[2:4]
			if num_dec != "00" and num_dec != "0":
				item.selling_price = int(item.selling_price + 1)
			item.sale_amount = flt(item.selling_price * item.qty)
			item.margin = item.sale_amount - item.cost_amount
		

	#new addition
	
	def validate_payment_terms_total(self):
		total = 0.00
		for data in self.get('payment_term_table'):
			val = data.value.replace("%", "")
			total += float(val)
		if total != 100.00:
			frappe.throw("Payment Terms total not equal to 100%")
			
	
	def validate_terms_checklist(self):
		if not self.get('terms_checklist'):
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
			
	
	def validate_deliverables(self):
		if not self.get('deliverables'):
			self.append("deliverables", {"topic": str(self.customer_name) + " approved " + str(self.solution) , "check": 0})
			self.append("deliverables", {"topic": "Training", "check": 0})
			self.append("deliverables", {"topic": "Operational and maintenance manual", "check": 0})
			self.append("deliverables", {"topic": "Maintenance for " + str(self.maintenance_support_period), "check": 0})
			self.append("deliverables", {"topic": "Check clock battery, replace if necessary", "check": 0})
		
	
	def validate_checklist(self):
		if not self.get('checklist_for_preventive_maintenance'):
			self.append("checklist_for_preventive_maintenance", {"topic": "Checking and functioning of all field devices like Dampers, Fans, Valves, sensors etc.", "check": 0})
			self.append("checklist_for_preventive_maintenance", {"topic": "The logics for each Chillers, AHUs, Primary Pumps, Secondary pumps, have to be thoroughly checked by changing the set point values, problems if any identified to be reported immediately.", "check": 0})
			self.append("checklist_for_preventive_maintenance", {"topic": "Carry out hardware and software diagnostic routine tasks and check computer orientation. Clean and check keyboard for correct operation.", "check": 0})
			self.append("checklist_for_preventive_maintenance", {"topic": "Clean and check conditions of sensors, field devices, cooling fans, lubricate if necessary.", "check": 0})
			self.append("checklist_for_preventive_maintenance", {"topic": "Check clock battery, replace if necessary", "check": 0})
			self.append("checklist_for_preventive_maintenance", {"topic": "Check monitor for correct focus, contrast, brightness and operation.", "check": 0})
			self.append("checklist_for_preventive_maintenance", {"topic": "Visually inspect the central station units and ensure that environmental conditions of all the equipment’s are within prescribed limits.", "check": 0})
			self.append("checklist_for_preventive_maintenance", {"topic": "Check cables and connectors for security, integrity and for a physical damage.", "check": 0})
			self.append("checklist_for_preventive_maintenance", {"topic": "Review existing data, alarm logs if necessary.", "check": 0})
			self.append("checklist_for_preventive_maintenance", {"topic": "Carry out voltage check on all power supplies, check standby batteries against manufacturer specifications", "check": 0})
			self.append("checklist_for_preventive_maintenance", {"topic": "Check operation of central control station units including modems, line drivers, and telemetry cable and interface unit.", "check": 0})
			self.append("checklist_for_preventive_maintenance", {"topic": "Check connectors security, integrity and for damage.", "check": 0})
			self.append("checklist_for_preventive_maintenance", {"topic": "Check mechanical and environmental conditions of outstation hardware.", "check": 0})
			self.append("checklist_for_preventive_maintenance", {"topic": "Check connector’s security, integrity, and for damage including security of incoming cables, prevention of ingress of moisture, door seals etc.", "check": 0})
			self.append("checklist_for_preventive_maintenance", {"topic": "Check integrity of data flow in both directions.", "check": 0})
			self.append("checklist_for_preventive_maintenance", {"topic": "Check plant alarm and software interlocks with safety implications if operating correctly.", "check": 0})
			self.append("checklist_for_preventive_maintenance", {"topic": "Check operation and interface of software interlocks to fire, security and access", "check": 0})
		if not self.get('checklist_for_reactive_maintenance'):
			self.append("checklist_for_reactive_maintenance", {"topic": "Customer will contact Tablix through Email or phone.", "check": 0})
			self.append("checklist_for_reactive_maintenance", {"topic": "It will redirect to customer care executive.", "check": 0})
			self.append("checklist_for_reactive_maintenance", {"topic": "An engineer will be notified to attend the call.", "check": 0})
			self.append("checklist_for_reactive_maintenance", {"topic": "The engineer will try to understand the problem on the telephone and try to provide telephonic assistance for first level resolution. ", "check": 0})
			self.append("checklist_for_reactive_maintenance", {"topic": "If onsite support is required, the Vendor Area Office will depute an engineer for technical assistance on site. ", "check": 0})
			self.append("checklist_for_reactive_maintenance", {"topic": "Any repair/ replacement of field equipment will be identified and will be quoted along with delivery time information. ", "check": 0})
			self.append("checklist_for_reactive_maintenance", {"topic": "Ladders/high rise ladders should be provided by customer at site to carry out PMS/rectification works. ", "check": 0})

	def total(self):
		self.total_cost = 0.0
		self.total_sale = 0.0
		self.service_cost = 0.0
		self.material_cost = 0.0
		site = ""
		cost_amt = 0.00
		sale_amt = 0.00
		to_remove = []
		no_of_days = 0.00
		amc_ppm_total = 0.00
		amc_rm_total = 0.00
		amc_spare_total = 0.00
		warranty_total = 0.00
		self.discount_perc = 0.00
		self.discount_amt = 0.00
		self.total_amt = 0.00
		self.amount_in_words = ""
		
		
		#BOQ
		self.total_cost = 0.00
		self.total_sale = 0.00
		cost_amt = 0.00
		sale_amt = 0.00
		self.discount_amt = 0.00
		if self.boq:
			for item in self.get("items"):
				item.opp_ref = self.opportunity
				if item.item_group == "Services":
					self.service_cost += item.cost_amount
					
				if item.site :
					#msgprint("Site: " + item.site)
					if site !="" and cost_amt !=0.00:
						#msgprint("Success")
						self.append("site_costing", {"site": site, "total_cost": cost_amt, "total_sale":sale_amt})
					site = item.site;
					cost_amt = 0.00;
					sale_amt = 0.00;
				self.total_cost += item.cost_amount
				self.total_sale += item.sale_amount
				cost_amt += item.cost_amount
				sale_amt += item.sale_amount
				
			self.append("site_costing", {"site": site, "total_cost": cost_amt, "total_sale":sale_amt})
			self.last_site_amt = sale_amt
			self.material_cost = self.total_cost - self.service_cost
			self.total_cost = self.total_cost + self.vat + self.duties + self.other_charges
			self.total_sale = self.total_sale + self.vat + self.duties + self.other_charges
			self.total_cost_amt = self.total_cost
			
			if (self.discount_ > 0.00 or self.special_discount > 0.00 or self.project_discount > 0.00 or self.special_project_discount > 0.00):
				discount_value = 0.00
				if self.discount_ > 0.00:
					if self.percentage and self.discount_ < 30:
						self.discount_ = self.total_sale *(float(self.discount_)/100)
					discount_value += float(self.discount_)
				if self.special_discount > 0.00:
					if self.percentage and self.special_discount < 30:
						self.special_discount = self.total_sale *(float(self.special_discount)/100)
					discount_value += float(self.special_discount)
				if self.project_discount > 0.00:
					if self.percentage and self.project_discount < 30:
						self.project_discount = self.total_sale *(float(self.project_discount)/100)
					discount_value += float(self.project_discount)
				if self.special_project_discount > 0.00:
					if self.percentage and self.special_project_discount < 30:
						self.special_project_discount = self.total_sale *(float(self.special_project_discount)/100)
					discount_value += float(self.special_project_discount)
				self.total_discount = discount_value
			else:
				self.total_discount = 0.00
			
			if self.total_discount and self.total_sale > 0:
				discount_amount = 0.00
				discount_amount = float(self.total_discount)
				self.discount_amt += discount_amount
				self.total_sale = self.total_sale - discount_amount
			
			if self.total_sale > 0:
				self.margin = self.total_sale - self.total_cost
				self.margin_percent = flt(self.margin)/ flt(self.total_sale)
				self.margin_percent = flt(self.margin_percent) * 100
				self.total_amt = self.total_sale
				self.amount_in_words = money_in_words(self.total_amt, self.currency)
			else:
				#msgprint("ELSE")
				self.margin = 0.00
				self.margin_percent = 0.00
				self.total_amt = 0.00
				self.amount_in_words = ""
				
			
		#AMC
		amc_total_amount = 0.00
		total_amc_charges = 0.00
		self.total_amc_months = 12
		if self.is_amc:
			self.total_cost_preventive_maintenance = 0.00
			self.total_cost_reactive_maintenance = 0.00
			self.total_cost_for_spare_parts = 0.00
			self.total_cost_preventive_maintenance_2nd_year = 0.00
			self.total_cost_reactive_maintenance_2nd_year = 0.00
			self.total_cost_for_spare_parts_2nd_year = 0.00
			self.total_cost_preventive_maintenance_3rd_year = 0.00
			self.total_cost_reactive_maintenance_3rd_year = 0.00
			self.total_cost_for_spare_parts_3rd_year = 0.00
			self.total_cost_preventive_maintenance_4th_year = 0.00
			self.total_cost_reactive_maintenance_4th_year = 0.00
			self.total_cost_for_spare_parts_4th_year = 0.00
			self.total_cost_preventive_maintenance_5th_year = 0.00
			self.total_cost_reactive_maintenance_5th_year = 0.00
			self.total_cost_for_spare_parts_5th_year = 0.00
			self.total_charges_of_maintenance = 0.00
			self.total_charges_of_maintenance_for_2nd_year = 0.00
			self.total_charges_of_maintenance_for_3rd_year = 0.00
			self.total_charges_of_maintenance_for_4th_year = 0.00
			self.total_charges_of_maintenance_for_5th_year = 0.00
			
			for items in self.get("amc_items"):
				items.opp_ref = self.opportunity
				
			amc_ppm_total = 0.00	
			for item1 in self.get("amc_preventive"):
				if item1.uom == "Days":
					no_of_days = item1.total
					
				elif item1.uom == "rate/day" :
					amc_ppm_total += (item1.total * no_of_days)
				
				else:
					amc_ppm_total += item1.total
			self.cost_for_ppm = amc_ppm_total
			
			if self.one_year_maintenance:
				self.total_cost_preventive_maintenance = self.cost_for_ppm * self.one_year_maintenance
				
			amc_rm_total = 0.00
			for item2 in self.get("amc_reactive"):
				amc_rm_total += item2.total
			self.cost_for_rm = amc_rm_total

			if self.no_of_calls:
				self.total_cost_reactive_maintenance = self.cost_for_rm * self.no_of_calls
				
			amc_spare_total = 0.00	
			for item3 in self.get("amc_spare_parts"):
				amc_spare_total += item3.amount
			self.total_cost_for_spare_parts = amc_spare_total
				
			
			if self.comprehensive:
				total_amc_charges = self.total_cost_preventive_maintenance + self.total_cost_reactive_maintenance + self.total_cost_for_spare_parts
				self.total_charges_of_maintenance = total_amc_charges
			else:
				total_amc_charges = self.total_cost_preventive_maintenance + self.total_cost_reactive_maintenance 
				self.total_charges_of_maintenance = total_amc_charges
				
				
			if self.percentage_applied_for_2nd_year:
				self.total_amc_months = 24
				self.total_cost_preventive_maintenance_2nd_year = self.total_cost_preventive_maintenance /(1-(float(self.percentage_applied_for_2nd_year)/100))
				self.total_cost_reactive_maintenance_2nd_year = self.total_cost_reactive_maintenance /(1-(float(self.percentage_applied_for_2nd_year)/100))
				if self.comprehensive:
					self.total_cost_for_spare_parts_2nd_year = self.total_cost_for_spare_parts /(1-(float(self.percentage_applied_for_2nd_year)/100))
				else:
					self.total_cost_for_spare_parts_2nd_year = 0.00
				self.total_charges_of_maintenance_for_2nd_year = self.total_cost_preventive_maintenance_2nd_year + self.total_cost_reactive_maintenance_2nd_year + self.total_cost_for_spare_parts_2nd_year
				
			if self.percentage_applied_for_3rd_year:
				self.total_amc_months = 36
				self.total_cost_preventive_maintenance_3rd_year = self.total_cost_preventive_maintenance /(1-(float(self.percentage_applied_for_3rd_year)/100))
				self.total_cost_reactive_maintenance_3rd_year = self.total_cost_reactive_maintenance /(1-(float(self.percentage_applied_for_3rd_year)/100))
				if self.comprehensive:
					self.total_cost_for_spare_parts_3rd_year = self.total_cost_for_spare_parts /(1-(float(self.percentage_applied_for_3rd_year)/100))
				else:
					self.total_cost_for_spare_parts_3rd_year = 0.00
				self.total_charges_of_maintenance_for_3rd_year = self.total_cost_preventive_maintenance_3rd_year + self.total_cost_reactive_maintenance_3rd_year + self.total_cost_for_spare_parts_3rd_year
				
			if self.percentage_applied_for_4th_year:
				self.total_amc_months = 48
				self.total_cost_preventive_maintenance_4th_year = self.total_cost_preventive_maintenance /(1-(float(self.percentage_applied_for_4th_year)/100))
				self.total_cost_reactive_maintenance_4th_year = self.total_cost_reactive_maintenance /(1-(float(self.percentage_applied_for_4th_year)/100))
				if self.comprehensive:
					self.total_cost_for_spare_parts_4th_year = self.total_cost_for_spare_parts /(1-(float(self.percentage_applied_for_4th_year)/100))
				else:
					self.total_cost_for_spare_parts_4th_year = 0.00
				self.total_charges_of_maintenance_for_4th_year = self.total_cost_preventive_maintenance_4th_year + self.total_cost_reactive_maintenance_4th_year + self.total_cost_for_spare_parts_4th_year
				
			if self.percentage_applied_for_5th_year:
				self.total_amc_months = 60
				self.total_cost_preventive_maintenance_5th_year = self.total_cost_preventive_maintenance /(1-(float(self.percentage_applied_for_5th_year)/100))
				self.total_cost_reactive_maintenance_5th_year = self.total_cost_reactive_maintenance /(1-(float(self.percentage_applied_for_5th_year)/100))
				if self.comprehensive:
					self.total_cost_for_spare_parts_5th_year = self.total_cost_for_spare_parts /(1-(float(self.percentage_applied_for_5th_year)/100))
				else:
					self.total_cost_for_spare_parts_5th_year = 0.00
				self.total_charges_of_maintenance_for_5th_year = self.total_cost_preventive_maintenance_5th_year + self.total_cost_reactive_maintenance_5th_year + self.total_cost_for_spare_parts_5th_year
			
			
			if self.amc_extended_warranty:
				i = 1
				for item4 in self.get("amc_extended_warranty"):
					warranty_total = item4.amount
					if i == 1:
						self.total_cost_for_spare_parts = self.total_cost_for_spare_parts + warranty_total
						self.total_charges_of_maintenance = self.total_charges_of_maintenance + warranty_total
					elif i == 2:
						self.total_cost_for_spare_parts_2nd_year = self.total_cost_for_spare_parts_2nd_year + warranty_total
						self.total_charges_of_maintenance_for_2nd_year =  self.total_charges_of_maintenance_for_2nd_year + warranty_total
					elif i == 3:
						self.total_cost_for_spare_parts_3rd_year = self.total_cost_for_spare_parts_3rd_year + warranty_total
						self.total_charges_of_maintenance_for_3rd_year =  self.total_charges_of_maintenance_for_3rd_year + warranty_total
					elif i == 4:
						self.total_cost_for_spare_parts_4th_year = self.total_cost_for_spare_parts_4th_year + warranty_total
						self.total_charges_of_maintenance_for_4th_year =  self.total_charges_of_maintenance_for_4th_year + warranty_total
					elif i == 5:
						self.total_cost_for_spare_parts_5th_year = self.total_cost_for_spare_parts_5th_year + warranty_total
						self.total_charges_of_maintenance_for_5th_year =  self.total_charges_of_maintenance_for_5th_year + warranty_total
					i = i + 1
				
				
			amc_total_amount = 0.00
			if self.total_charges_of_maintenance > 0:
				amc_total_amount += self.total_charges_of_maintenance
			if self.total_charges_of_maintenance_for_2nd_year > 0:
				amc_total_amount += self.total_charges_of_maintenance_for_2nd_year
			if self.total_charges_of_maintenance_for_3rd_year > 0:
				amc_total_amount += self.total_charges_of_maintenance_for_3rd_year
			if self.total_charges_of_maintenance_for_4th_year > 0:
				amc_total_amount += self.total_charges_of_maintenance_for_4th_year
			if self.total_charges_of_maintenance_for_5th_year > 0:
				amc_total_amount += self.total_charges_of_maintenance_for_5th_year
			self.amc_total_cost = amc_total_amount
			self.total_cost_amt = self.amc_total_cost
			
			
			
			if self.amc_applied_margin_percent:
				if self.total_charges_of_maintenance > 0:
					self.total_cost_preventive_maintenance = self.total_cost_preventive_maintenance /(1-(float(self.amc_applied_margin_percent)/100))
					self.total_cost_reactive_maintenance = self.total_cost_reactive_maintenance /(1-(float(self.amc_applied_margin_percent)/100))
					if self.comprehensive:
						self.total_cost_for_spare_parts = self.total_cost_for_spare_parts/(1-(float(self.amc_applied_margin_percent)/100))
					else:
						self.total_cost_for_spare_parts = 0.00
					self.total_charges_of_maintenance = self.total_cost_preventive_maintenance + self.total_cost_reactive_maintenance + self.total_cost_for_spare_parts
				
				if self.total_charges_of_maintenance_for_2nd_year > 0:
					self.total_cost_preventive_maintenance_2nd_year = self.total_cost_preventive_maintenance_2nd_year /(1-(float(self.amc_applied_margin_percent)/100))
					self.total_cost_reactive_maintenance_2nd_year = self.total_cost_reactive_maintenance_2nd_year /(1-(float(self.amc_applied_margin_percent)/100))
					if self.comprehensive:
						self.total_cost_for_spare_parts_2nd_year = self.total_cost_for_spare_parts_2nd_year /(1-(float(self.amc_applied_margin_percent)/100))
					else:
						self.total_cost_for_spare_parts_2nd_year = 0.00
					self.total_charges_of_maintenance_for_2nd_year = self.total_cost_preventive_maintenance_2nd_year + self.total_cost_reactive_maintenance_2nd_year + self.total_cost_for_spare_parts_2nd_year
				
				if self.total_charges_of_maintenance_for_3rd_year > 0:
					self.total_cost_preventive_maintenance_3rd_year = self.total_cost_preventive_maintenance_3rd_year /(1-(float(self.amc_applied_margin_percent)/100))
					self.total_cost_reactive_maintenance_3rd_year = self.total_cost_reactive_maintenance_3rd_year /(1-(float(self.amc_applied_margin_percent)/100))
					if self.comprehensive:
						self.total_cost_for_spare_parts_3rd_year = self.total_cost_for_spare_parts_3rd_year /(1-(float(self.amc_applied_margin_percent)/100))
					else:
						total_cost_for_spare_parts_3rd_year = 0.00
					self.total_charges_of_maintenance_for_3rd_year = self.total_cost_preventive_maintenance_3rd_year + self.total_cost_reactive_maintenance_3rd_year + self.total_cost_for_spare_parts_3rd_year
					
				if self.total_charges_of_maintenance_for_4th_year > 0:
					self.total_cost_preventive_maintenance_4th_year = self.total_cost_preventive_maintenance_4th_year /(1-(float(self.amc_applied_margin_percent)/100))
					self.total_cost_reactive_maintenance_4th_year = self.total_cost_reactive_maintenance_4th_year /(1-(float(self.amc_applied_margin_percent)/100))
					if self.comprehensive:
						self.total_cost_for_spare_parts_4th_year = self.total_cost_for_spare_parts_4th_year /(1-(float(self.amc_applied_margin_percent)/100))
					else:
						total_cost_for_spare_parts_4th_year = 0.00
					self.total_charges_of_maintenance_for_4th_year = self.total_cost_preventive_maintenance_4th_year + self.total_cost_reactive_maintenance_4th_year + self.total_cost_for_spare_parts_4th_year
					
				if self.total_charges_of_maintenance_for_5th_year > 0:
					self.total_cost_preventive_maintenance_5th_year = self.total_cost_preventive_maintenance_5th_year /(1-(float(self.amc_applied_margin_percent)/100))
					self.total_cost_reactive_maintenance_5th_year = self.total_cost_reactive_maintenance_5th_year /(1-(float(self.amc_applied_margin_percent)/100))
					if self.comprehensive:
						self.total_cost_for_spare_parts_5th_year = self.total_cost_for_spare_parts_5th_year /(1-(float(self.amc_applied_margin_percent)/100))
					else:
						total_cost_for_spare_parts_5th_year = 0.00
					self.total_charges_of_maintenance_for_5th_year = self.total_cost_preventive_maintenance_5th_year + self.total_cost_reactive_maintenance_5th_year + self.total_cost_for_spare_parts_5th_year
				
				if self.amc_extended_warranty:
					i = 1
					for item4 in self.get("amc_extended_warranty"):
						warranty_total = item4.amount
						if i == 1:
							self.total_cost_for_spare_parts = self.total_cost_for_spare_parts + (warranty_total/(1-(float(self.amc_applied_margin_percent)/100)))
							self.total_charges_of_maintenance = self.total_charges_of_maintenance + (warranty_total/(1-(float(self.amc_applied_margin_percent)/100)))
						elif i == 2:
							self.total_cost_for_spare_parts_2nd_year = self.total_cost_for_spare_parts_2nd_year + (warranty_total/(1-(float(self.amc_applied_margin_percent)/100)))
							self.total_charges_of_maintenance_for_2nd_year =  self.total_charges_of_maintenance_for_2nd_year + (warranty_total/(1-(float(self.amc_applied_margin_percent)/100)))
						elif i == 3:
							self.total_cost_for_spare_parts_3rd_year = self.total_cost_for_spare_parts_3rd_year + (warranty_total/(1-(float(self.amc_applied_margin_percent)/100)))
							self.total_charges_of_maintenance_for_3rd_year =  self.total_charges_of_maintenance_for_3rd_year + (warranty_total/(1-(float(self.amc_applied_margin_percent)/100)))
						elif i == 4:
							self.total_cost_for_spare_parts_4th_year = self.total_cost_for_spare_parts_4th_year + (warranty_total/(1-(float(self.amc_applied_margin_percent)/100)))
							self.total_charges_of_maintenance_for_4th_year =  self.total_charges_of_maintenance_for_4th_year + (warranty_total/(1-(float(self.amc_applied_margin_percent)/100)))
						elif i == 5:
							self.total_cost_for_spare_parts_5th_year = self.total_cost_for_spare_parts_5th_year + (warranty_total/(1-(float(self.amc_applied_margin_percent)/100)))
							self.total_charges_of_maintenance_for_5th_year =  self.total_charges_of_maintenance_for_5th_year + (warranty_total/(1-(float(self.amc_applied_margin_percent)/100)))
						i = i + 1	
					
				self.amc_total_sale_ = self.total_charges_of_maintenance + self.total_charges_of_maintenance_for_2nd_year + self.total_charges_of_maintenance_for_3rd_year + self.total_charges_of_maintenance_for_4th_year + self.total_charges_of_maintenance_for_5th_year
			else:
				self.amc_total_sale_ = 0.00

			
			to_remove = []
			for d in self.get("amc_total"):
				to_remove.append(d)
			[self.remove(d) for d in to_remove]
			
			if self.total_charges_of_maintenance > 0:
				self.append("amc_total", {"item_code": "AMC 1st year" , "item_name": "Annual Maintenance Contract for 1st year", "description": "Annual Maintenance Contract for 1st year", "stock_uom": "Nos", "qty":1, "rate": self.total_charges_of_maintenance, "amount": self.total_charges_of_maintenance, "item_group": "Annual Maintenance Contract"})
			if self.total_charges_of_maintenance_for_2nd_year > 0:
				self.append("amc_total", {"item_code": "AMC 2nd year" , "item_name": "Annual Maintenance Contract for 2nd year", "description": "Annual Maintenance Contract for 2nd year", "stock_uom": "Nos", "qty":1, "rate": self.total_charges_of_maintenance_for_2nd_year, "amount": self.total_charges_of_maintenance_for_2nd_year, "item_group": "Annual Maintenance Contract"})
			if self.total_charges_of_maintenance_for_3rd_year > 0:
				self.append("amc_total", {"item_code": "AMC 3rd year" , "item_name": "Annual Maintenance Contract for 3rd year", "description": "Annual Maintenance Contract for 3rd year", "stock_uom": "Nos", "qty":1, "rate": self.total_charges_of_maintenance_for_3rd_year, "amount": self.total_charges_of_maintenance_for_3rd_year, "item_group": "Annual Maintenance Contract"})
			if self.total_charges_of_maintenance_for_4th_year > 0:
				self.append("amc_total", {"item_code": "AMC 4th year" , "item_name": "Annual Maintenance Contract for 4th year", "description": "Annual Maintenance Contract for 4th year", "stock_uom": "Nos", "qty":1, "rate": self.total_charges_of_maintenance_for_4th_year, "amount": self.total_charges_of_maintenance_for_4th_year, "item_group": "Annual Maintenance Contract"})
			if self.total_charges_of_maintenance_for_5th_year > 0:
				self.append("amc_total", {"item_code": "AMC 5th year" , "item_name": "Annual Maintenance Contract for 5th year", "description": "Annual Maintenance Contract for 5th year", "stock_uom": "Nos", "qty":1, "rate": self.total_charges_of_maintenance_for_5th_year, "amount": self.total_charges_of_maintenance_for_5th_year, "item_group": "Annual Maintenance Contract"})

			
			if (self.amc_discount_ > 0.00 or self.amc_special_discount > 0.00 or self.amc_project_discount > 0.00 or self.amc_special_project_discount > 0.00):
				discount_value = 0.00
				if self.amc_discount_ > 0.00:
					if self.percentage and self.amc_discount_ < 30:
						self.amc_discount_ = self.total_sale *(float(self.amc_discount_)/100)
					discount_value += float(self.amc_discount_)
				if self.amc_special_discount > 0.00:
					if self.percentage and self.amc_special_discount < 30:
						self.amc_special_discount = self.total_sale *(float(self.amc_special_discount)/100)
					discount_value += float(self.amc_special_discount)
				if self.amc_project_discount > 0.00:
					if self.percentage and self.amc_project_discount < 30:
						self.amc_project_discount = self.total_sale *(float(self.amc_project_discount)/100)
					discount_value += float(self.amc_project_discount)
				if self.amc_special_project_discount > 0.00:
					if self.percentage and self.amc_special_project_discount < 30:
						self.amc_special_project_discount = self.total_sale *(float(self.amc_special_project_discount)/100)
					discount_value += float(self.amc_special_project_discount)
				self.total_amc_discount = discount_value
			else:
				self.total_amc_discount = 0.00
				
			if self.total_amc_discount and self.amc_total_sale_ > 0:
				discount_amount = 0.00
				discount_amount = float(self.total_amc_discount)
				self.discount_amt += discount_amount		
				self.amc_total_sale_ = self.amc_total_sale_ - discount_amount
			
			if self.amc_total_sale_ > 0:
				self.amc_margin = self.amc_total_sale_ - self.amc_total_cost
				self.amc_margin_percent = flt(self.amc_margin)/ flt(self.amc_total_sale_)
				self.amc_margin_percent = flt(self.amc_margin_percent) * 100
			
			if self.amc_total_sale_:
				self.total_amt = self.amc_total_sale_
				self.amount_in_words = money_in_words(self.total_amt, self.currency)
		
		if self.boq == 1 and self.is_amc == 1:
			self.total_cost_amt = self.total_cost + self.amc_total_cost
			self.total_amt = self.total_sale + self.amc_total_sale_
			self.amount_in_words = money_in_words(self.total_amt, self.currency)
			
			
	# new addition
	
	def send_notification(self, reason, comment=""):
		project_name = frappe.db.get_value("Boq", self.name, 'project_site_name')
		bdm = frappe.db.get_value("Boq", self.name, 'bdm')
		customer_name = frappe.db.get_value("Boq", self.name, 'customer_name')
		#msgprint("Entry")
		if reason == "site_survey":
			val = 5
			self.notify_employee(bdm, project_name, val, customer_name)
			if bdm == "gopu@tablix.ae" or bdm == "kartik@tablix.ae":
				self.notify_employee(sales_coordinator_rep, project_name, val, customer_name)
			frappe.db.set_value("Boq", self.name, "status", "Site Survey")
			frappe.db.commit()	
			
		elif reason == "designing":
			#revert_status = frappe.db.get_value("Boq", self.name, "revert_status")
			revert_status = 0
			if comment != "":
				revert_status = 1
				frappe.db.set_value("Boq", self.name, "margin_comment", comment)
			if revert_status:
				val = 9
				self.notify_employee(self.created_by, project_name, val, customer_name)
			val = 6
			self.notify_employee(bdm, project_name, val, customer_name)
			if bdm == "gopu@tablix.ae" or bdm == "kartik@tablix.ae":
				self.notify_employee(sales_coordinator_rep, project_name, val, customer_name)
			frappe.db.set_value("Boq", self.name, "status", "Designing")
			frappe.db.commit()
		
		elif reason == "costing":
			val = 0
			costing_rep = "ali@tablix.ae"
			
			task_sett = frappe.db.get_values('Commercial Task Settings',{'parent':'Buying Settings'}, ['module','upper_amount','lower_amount','tablix_rep'])
			for i in task_sett:
				if str(i[0]) == 'BOQ':
					upper_amount = float(i[1])
					lower_amount = float(i[2])
					if self.boq:
						if self.total_cost >= lower_amount and self.total_cost <= upper_amount :
							costing_rep = str(i[3])
					elif self.is_amc:
						if self.total_charges_of_maintenance  >= lower_amount and self.total_charges_of_maintenance <= upper_amount :
							costing_rep = str(i[3])
			if comment != "":
				frappe.db.set_value("Boq", self.name, "margin_comment", comment)
			self.notify_employee(costing_rep, project_name, val, customer_name)
			val = 7.1
			self.notify_employee(commercial_mgmr, project_name, val, customer_name)
			self.notify_employee(bdm, project_name, val, customer_name)
			if bdm == "gopu@tablix.ae" or bdm == "kartik@tablix.ae":
				self.notify_employee(sales_coordinator_rep, project_name, val, customer_name)
			frappe.db.set_value("Boq", self.name, "status", "Costing")
			cur_date=datetime.datetime.now()
			cur_date = cur_date.strftime("%Y-%m-%d %H:%M:%S")
			frappe.db.set_value("Boq", self.name, "costing_", cur_date)
			#frappe.db.set_value("Boq", self.name, "revert_status", False)
			frappe.db.commit()	
		
		elif reason == "cto_verify":
			val = 8
			self.notify_employee(cto, project_name, val, customer_name)
			val = 7.2
			self.notify_employee(bdm, project_name, val, customer_name)
			if bdm == "gopu@tablix.ae" or bdm == "kartik@tablix.ae":
				self.notify_employee(sales_coordinator_rep, project_name, val, customer_name)
			frappe.db.set_value("Boq", self.name, "status", "CTO Verification")
			frappe.db.set_value("Boq", self.name, "revert_status", False)
			frappe.db.set_value("Boq", self.name, "margin_comment", "")
			frappe.db.commit()	
			
		elif reason == "boq_complete":
			val = 1
			if bdm == "gopu@tablix.ae" or bdm == "kartik@tablix.ae":
				self.notify_employee(sales_coordinator_rep, project_name, val, customer_name)
				val = 11
				self.notify_employee(bdm, project_name, val, customer_name)
			else:
				self.notify_employee(bdm, project_name, val, customer_name)
			frappe.db.set_value("Boq", self.name, "status", "Boq Complete")
			frappe.db.set_value("Boq", self.name, "margin_comment", "")
			frappe.db.commit()
			
		elif reason == "sales_margin":
			val = 2
			acc_manager = frappe.db.get_value("Boq", self.name, 'account_manager')
			frappe.db.set_value("Boq", self.name, "status", "BDM Verified")
			cur_date=datetime.datetime.now()
			cur_date = cur_date.strftime("%Y-%m-%d %H:%M:%S")
			frappe.db.set_value("Boq", self.name, "bdm_date_time", cur_date)
			self.notify_employee(acc_manager, project_name, val, customer_name)
			frappe.db.set_value("Boq", self.name, "margin_comment", comment)
			frappe.db.commit()
		
		elif reason == "cbdo_sales_margin":
			val = 2
			acc_manager = frappe.db.get_value("Boq", self.name, 'account_manager')
			if acc_manager == cbdo:
				frappe.db.set_value("Boq", self.name, "status", "CBDO Approved")
				cur_date=datetime.datetime.now()
				cur_date = cur_date.strftime("%Y-%m-%d %H:%M:%S")
				frappe.db.set_value("Boq", self.name, "cbdo_date_time", cur_date)
				self.notify_employee(finance_emp, project_name, val, customer_name)
			else:
				frappe.db.set_value("Boq", self.name, "status", "KAM Approved")
				cur_date=datetime.datetime.now()
				cur_date = cur_date.strftime("%Y-%m-%d %H:%M:%S")
				frappe.db.set_value("Boq", self.name, "kam_date_time", cur_date)
				self.notify_employee(cbdo, project_name, val, customer_name)
				
			frappe.db.set_value("Boq", self.name, "revert_status", False)		
			frappe.db.set_value("Boq", self.name, "margin_comment", "")
			val = 10.1
			self.notify_employee(bdm, project_name, val, customer_name)
			if bdm == "gopu@tablix.ae" or bdm == "kartik@tablix.ae":
				self.notify_employee(sales_coordinator_rep, project_name, val, customer_name)
			frappe.db.commit()
			
		elif reason == "finance_pay_terms":
			val = 2
			frappe.db.set_value("Boq", self.name, "status", "CBDO Approved")
			frappe.db.set_value("Boq", self.name, "revert_status", False)
			frappe.db.set_value("Boq", self.name, "margin_comment", "")
			self.notify_employee(finance_emp, project_name, val, customer_name)
			val = 10.2
			self.notify_employee(bdm, project_name, val, customer_name)
			if bdm == "gopu@tablix.ae" or bdm == "kartik@tablix.ae":
				self.notify_employee(sales_coordinator_rep, project_name, val, customer_name)
			frappe.db.commit()
		
		elif reason == "sam_disapprove":
			val = 4
			acc_manager = frappe.db.get_value("Boq", self.name, 'account_manager')
			frappe.db.set_value("Boq", self.name, "status", "KAM Disapproved")
			frappe.db.set_value("Boq", self.name, "margin_comment", comment)
			if bdm == "gopu@tablix.ae" or bdm == "kartik@tablix.ae":
				self.notify_employee(sales_coordinator_rep, project_name, val, customer_name)
				val = 12
				self.notify_employee(bdm, project_name, val, customer_name)
			else:
				self.notify_employee(bdm, project_name, val, customer_name)
			frappe.db.commit()
			
		elif reason == "cbdo_disapprove":
			val = 4.1
			frappe.db.set_value("Boq", self.name, "status", "CBDO Disapproved")
			frappe.db.set_value("Boq", self.name, "margin_comment", comment)
			if bdm == "gopu@tablix.ae" or bdm == "kartik@tablix.ae":
				self.notify_employee(sales_coordinator_rep, project_name, val, customer_name)
				val = 12.1
				self.notify_employee(bdm, project_name, val, customer_name)
			else:
				self.notify_employee(bdm, project_name, val, customer_name)
			frappe.db.commit()
			
		elif reason == "finance_disapprove":
			val = 4.2
			frappe.db.set_value("Boq", self.name, "status", "Finance Disapproved")
			frappe.db.set_value("Boq", self.name, "margin_comment", comment)
			if bdm == "gopu@tablix.ae" or bdm == "kartik@tablix.ae":
				self.notify_employee(sales_coordinator_rep, project_name, val, customer_name)
				val = 12.2
				self.notify_employee(bdm, project_name, val, customer_name)
			else:
				self.notify_employee(bdm, project_name, val, customer_name)
			frappe.db.commit()
			
		else:
			val = 3
			frappe.db.set_value("Boq", self.name, "status", "Sales Complete")
			frappe.db.set_value("Boq", self.name, "revert_status", False)
			frappe.db.set_value("Boq", self.name, "margin_comment", "")
			self.notify_employee(bdm, project_name, val, customer_name)
			if bdm == "gopu@tablix.ae" or bdm == "kartik@tablix.ae":
				self.notify_employee(sales_coordinator_rep, project_name, val, customer_name)
				val = 13
				self.notify_employee(bdm, project_name, val, customer_name)
			else:
				self.notify_employee(bdm, project_name, val, customer_name)
			frappe.db.commit()
			
		
		return True
	
	
	
	
	def notify_employee(self, employee, subject, val, customer):
		
		
		#msgprint("Success" + str(val))
		
		def _get_message(url=False):
			if url:
				name = get_link_to_form(self.doctype, self.name)
			else:
				name = self.name
			if val == 0:
				return (_("BOQ")+ "- %s of %s " + _("assigned for Costing") + ": %s") % (subject, customer, name)
			elif val ==1:
				return (_("BOQ")+ "- %s of %s " + _("assigned for Sales Margin/Discount Addition") + ": %s") % (subject, customer, name)
			elif val == 2:
				return (_("BOQ")+ "- %s of %s " + _("requires Sales Margin Approval") + ": %s") % (subject, customer, name)
			elif val == 5:
				return (_("BOQ")+ "- %s of %s " + _("is in Site Survey stage now") + ": %s") % (subject, customer, name)
			elif val == 6:
				return (_("BOQ")+ "- %s of %s " + _("is in Designing stage now") + ": %s") % (subject, customer, name)
			elif val == 7.1:
				return (_("BOQ")+ "- %s of %s " + _("is in Costing stage now") + ": %s") % (subject, customer, name)	
			elif val == 7.2:
				return (_("BOQ")+ "- %s of %s " + _("is in CTO Verification stage now") + ": %s") % (subject, customer, name)
			elif val == 8:
				return (_("BOQ")+ "- %s of %s " + _("assigned for CTO Verification") + ": %s") % (subject, customer, name)
			elif val == 9:
				return (_("BOQ")+ "- %s of %s " + _("Boq requires verification") + ": %s") % (subject, customer, name)
			elif val == 4:
				return (_("BOQ")+ "- %s of %s " + _("Boq disapproved by KAM") + ": %s") % (subject, customer, name)
			elif val == 4.1:
				return (_("BOQ")+ "- %s of %s " + _("Boq disapproved by CBDO") + ": %s") % (subject, customer, name)
			elif val == 4.2:
				return (_("BOQ")+ "- %s of %s " + _("Boq disapproved by CFO") + ": %s") % (subject, customer, name)
			elif val == 10.1:
				return (_("BOQ")+ "- %s of %s " + _("Boq approved by KAM") + ": %s") % (subject, customer, name)
			elif val == 10.2:
				return (_("BOQ")+ "- %s of %s " + _("Boq approved by CBDO") + ": %s") % (subject, customer, name)
			elif val == 11:
				return (_("BOQ")+ "- %s of %s " + _("assigned to Sales Co-ordinator for Sales Margin/Discount Addition") + ": %s") % (subject, customer, name)
			elif val == 12:
				return (_("BOQ")+ "- %s of %s " + _("Boq disapproved by KAM") + ": %s") % (subject, customer, name)
			elif val == 12.1:
				return (_("BOQ")+ "- %s of %s " + _("Boq disapproved by CBDO") + ": %s") % (subject, customer, name)
			elif val == 12.2:
				return (_("BOQ")+ "- %s of %s " + _("Boq disapproved by CFO") + ": %s") % (subject, customer, name)
			elif val == 13:
				return (_("BOQ")+ "- %s of %s " + _("Boq approved by CFO for creating Quotation.") + ": %s") % (subject, customer, name)
			else:
				return (_("BOQ")+ "- %s of %s " + _("Boq approved by CFO") + ": %s") % (subject, customer, name)
			
		
			
		self.notify({
			# for post in messages
			"message": _get_message(url=True),
			"message_to": employee,
			"subject": _get_message(),
			"subject": _get_message(),
		})
	
		desc = ''	
		if val != 5 and val != 6 and val != 7.1 and val != 7.2 and val != 10.1 and val != 10.2 and val != 11 and val != 12 and val != 12.1 and val != 12.2 and val != 13 :
			assign_to.clear(self.doctype, self.name)
			proj_name = self.project_site_name.encode('ascii','ignore')
			if val == 0:
				desc = "BOQ- " + str(proj_name) + " assigned for Costing"
			elif val == 1:
				desc = "BOQ- " + str(proj_name) + " assigned for Sales Margin Approval"
			elif val == 2:
				desc = "BOQ- " + str(proj_name) + " requires Approval for Sales Margin Details"
			elif val == 8:
				desc = "BOQ- " + str(proj_name) + " requires CTO Verfification as BOQ Cost exceeded 500000"
			elif val == 9:
				desc = "BOQ- " + str(proj_name) + " requires Verfication"
			elif val == 4:
				desc = "BOQ- " + str(proj_name) + " disapproved by KAM"
			elif val == 4.1:
				desc = "BOQ- " + str(proj_name) + " disapproved by CBDO"
			elif val == 4.2:
				desc = "BOQ- " + str(proj_name) + " disapproved by CFO"
			elif val == 3:
				desc = "BOQ- " + str(proj_name) + " approved by CFO"
				
			assign_to.add({
				"assign_to": employee,
				"doctype": self.doctype,
				"name": self.name,
				"description": desc
		})
		
		
	def notify(self, args):
		args = frappe._dict(args)
		from frappe.desk.page.chat.chat import post
		post(**{"txt": args.message, "contact": args.message_to, "subject": args.subject, "notify": 1})
		
		
		
		
	#new addition
	
	def validate_proposal(self):
		
		if self.status  == "Designing" and self.boq and not self.boq_type:
			frappe.throw(_("Please enter BoQ Type !!!"))
		if self.status  == "Designing" and self.is_amc and not self.amc_duration:
			frappe.throw(_("Please enter AMC Duration !!!"))
		if self.status  == "Designing" and self.is_amc and (not self.comprehensive and not self.non_comprehensive):
			frappe.throw(_("Please enter AMC Type !!!"))
			
		if self.status  == "Boq Complete" and self.is_amc and not self.support_timings:
			frappe.throw(_("Please enter Support timings !!!"))
		if self.status  == "Boq Complete" and self.is_amc and not self.type_of_support:
			frappe.throw(_("Please enter Type of Support !!!"))
		if self.status  == "Boq Complete" and self.is_amc and not self.response_commitment:
			frappe.throw(_("Please enter Response Commitment!!!"))
		if self.status  == "Boq Complete" and self.is_amc and not self.resolution_commitment:
			frappe.throw(_("Please enter Resolution Commitment !!!"))
		if self.status  == "Designing" and self.is_amc and not self.amc_items:
			frappe.throw(_("Please enter AMC Items !!!"))
		if self.status  == "Designing" and self.is_amc and not self.amc_preventive:
			frappe.throw(_("Please enter AMC Preventive Items !!!"))
		if self.status  == "Designing" and self.is_amc and not self.amc_reactive:
			frappe.throw(_("Please enter AMC Reactive Items !!!"))
		#if self.status  == "Designing" and self.is_amc and self.comprehensive and not self.amc_spare_parts:
		#	frappe.throw(_("Please enter AMC Spare Parts Items !!!"))
		if self.status  == "Designing" and self.is_amc and not self.one_year_maintenance:
			frappe.throw(_("Please enter No. of PPM required in One year !!!"))
		if self.status  == "Designing" and self.is_amc and not self.no_of_calls:
			frappe.throw(_("Please enter No. of calls required in One year for Reactive maintenance !!!"))
			
			
		if self.status  == "Designing" and self.boq and not self.items:
			frappe.throw(_("Please enter Item Details with Costing !!!"))
		if self.status  == "Designing" and not self.our_scope:
			frappe.throw(_("Please enter Proposal Name !!!"))
		if self.status  == "Designing" and not self.solution:
			frappe.throw(_("Please enter Solution Name !!!"))
			
		if self.status  == "Boq Complete" and self.boq and not self.applied_margin_percent:
			frappe.throw(_("Please enter desired Margin for Boq !!!"))
		if self.status  == "Boq Complete" and self.is_amc and not self.amc_applied_margin_percent:
			frappe.throw(_("Please enter desired Margin for AMC !!!"))
		if self.status  == "Boq Complete" and not self.payment_term_table:
			frappe.throw(_("Please enter Payment Terms !!!"))
			
		#if self.status  == "Boq Complete" and (not self.payment_days or self.payment_days <=0):
		#	frappe.throw(_("Please enter Payment Days !!!"))
		if self.status  == "Designing" and self.boq and self.boq_type != "Supply" and (not self.proposed_project_completion_time or self.proposed_project_completion_time <= 0) :
			frappe.throw(_("Please enter Estimated Project Implementation Time !!!"))
		if self.status  == "Costing" and self.boq and (not self.mobilization_period or self.mobilization_period <= 0):
			frappe.throw(_("Please enter Mobilization Period !!!"))
		if self.status  == "Costing" and self.boq and (not self.maintenance_support_period or self.maintenance_support_period <=0) :
			frappe.throw(_("Please enter Maintenance/Support Period !!!"))
		if self.status  == "Boq Complete"  and self.boq and (not self.validity_of_proposal or self.validity_of_proposal <=0):
			frappe.throw(_("Please enter Validity of Proposal !!!"))
		if self.status  == "Costing" and self.boq and (not self.dlp_period or self.dlp_period <=0):
			frappe.throw(_("Please enter DLP Period !!!"))
			
		if self.status  == "Designing" and self.boq and self.is_proposal and not self.requirements_vs_solution_:
			frappe.throw(_("Please enter REQ VS SOLUTION !!!"))
		if self.status  == "Designing" and self.boq and self.is_proposal and not self.product_overview:
			frappe.throw(_("Please enter PRODUCT OVERVIEW !!!"))
		if self.status  == "Designing" and self.boq and self.is_proposal and not self.upload_site_image:
			frappe.throw(_("Please Upload Site Image with Site name !!!"))
		if self.status  == "Boq Complete" and self.boq and self.is_proposal and not self.deliverables:
			frappe.throw(_("Please enter Deliverable details!!!"))
		if self.status  == "Boq Complete" and self.boq and self.is_proposal and not self.system_overview:
			frappe.throw(_("Please enter System Overview details!!!"))
		if self.status  == "Designing" and not self.scope_of_work:
			frappe.throw(_("Please enter Scope of Work !!!"))
		if self.status  == "Designing" and not self.exclusions:
			frappe.throw(_("Please enter Exclusions !!!"))
		
		
	#new addition
	
	def costing_time():
		sql="""select name , account_manager , Date_Format(costing_ , "%Y-%m-%d %H:%i:%s" ) As date, costing_mail_time from tabBoq where status = 'Costing'"""
		var=frappe.db.sql(sql)
		#frappe.msgprint(str(var))
		for e in var:
			if e[2] is not None and e[2] != "":
				nm = []
				scnd =[]
				final = ""
				name = ""
				nm = e[1].split("@")
				if nm != []:
					name = str(nm[0])
					if "." in name:
						scnd = name.split(".")
						final = str(scnd[0])
					else:
						final = name
				fmt = '%Y-%m-%d %H:%M:%S'
				date1 = datetime.datetime.strptime(e[2], fmt)
				date1 = datetime.datetime.strftime(date1, fmt)
				date2 = datetime.datetime.now()
				date2 = datetime.datetime.strftime(date2, fmt)
				datediff = frappe.utils.data.time_diff(date2, date1)
				datediff = datediff.__str__()
				#frappe.msgprint(datediff)
				total_hrs = 0.00
				hour_str = [] 
				no_of_hours = []
				no_of_days = ""
				incr = 0
				hour_str = datediff.split(",")
				if hour_str != []:
					no_of_days = str(hour_str[0])
					#msgprint(no_of_days)
					if(("days" in no_of_days) or ('day' in no_of_days)) :
						if "days" in no_of_days :
							no_of_days = float(no_of_days.replace(" days", ""))
						else:
							no_of_days = float(no_of_days.replace(" day", ""))
						no_of_days = no_of_days *24*60*60
						no_of_hours = hour_str[1].split(":")
						if no_of_hours != []:
							hrs = float(no_of_hours[0]) *60*60
							mins = float(no_of_hours[1]) *60
							secs = float(no_of_hours[2])
							total_seconds = no_of_days + hrs + mins + secs
							total_hrs = total_seconds / 3600
							#msgprint(str(total_hrs))
					else:
						no_of_hours = hour_str[0].split(":")
						if no_of_hours != []:
							hrs = float(no_of_hours[0]) *60*60
							mins = float(no_of_hours[1]) *60
							secs = float(no_of_hours[2])
							total_seconds = hrs + mins + secs
							total_hrs = total_seconds / 3600
							#msgprint(str(total_hrs))
					#frappe.msgprint(str(e[3]))
					#frappe.msgprint("Hello")
					if total_hrs >= 72 and e[3]<=3:
						rm=int(e[3])
						rm = rm +1
						incr =int(rm)
						#frappe.msgprint(str(incr))
					elif total_hrs >= 72 and e[3]>3:
						incr = e[3]
					frappe.db.set_value("Boq", e[0], "costing_mail_time", incr)
					#frappe.msgprint("Updated")
					if total_hrs >= 72 and e[3]<=3:
						costing_rep = "ali@tablix.ae"
						task_sett = frappe.db.get_values('Commercial Task Settings',{'parent':'Buying Settings'}, ['module','upper_amount','lower_amount','tablix_rep'])
						for i in task_sett:
							if str(i[0]) == 'BOQ':
								upper_amount = float(i[1])
								lower_amount = float(i[2])
							if self.boq:
								if self.total_cost >= lower_amount and self.total_cost <= upper_amount :
									costing_rep = str(i[3])
							elif self.is_amc:
								if self.total_charges_of_maintenance  >= lower_amount and self.total_charges_of_maintenance <= upper_amount :
									costing_rep = str(i[3])
						html = """<html><head></head><body><p>"""+ e[0] + """ is pending for Approval</p></body></html>"""
						frappe.sendmail(recipients = costing_rep,
							subject=_("{0} is pending for Approvel").format(e[0]),
							message=_("""{0}""").format(html),
							reply_to= costing_rep)
					elif total_hrs >= 72 and e[3] > 3:
						html = """<html><head></head><body><p>"""+ e[0] + """ is not approved by """ +final+ """ </p></body></html>"""
						frappe.sendmail(recipients = "gopu@tablix.ae",
							subject=_("{0} is pending for Approvel").format(e[0]),
							message=_("""{0}""").format(html),
							reply_to= "gopu@tablix.ae")
					else:
						frappe.msgprint("Email is not sent")
						
	def bdm_time():
		sql="""select name , account_manager , Date_Format(bdm_date_time , "%Y-%m-%d %H:%i:%s") As date, bdm_mail_time from tabBoq where status = 'BDM Verified'"""
		var=frappe.db.sql(sql)
		#frappe.msgprint(str(var))
		for e in var:
			if e[2] is not None and e[2] != "":
				nm = []
				scnd =[] 
				final = ""
				name = ""
				nm = e[1].split("@")
				if nm != []:
					name = str(nm[0])
					if "." in name:
						scnd = name.split(".")
						final = str(scnd[0])
					else:
						final = name
				fmt = '%Y-%m-%d %H:%M:%S'
				date1 = datetime.datetime.strptime(e[2], fmt)
				date1 = datetime.datetime.strftime(date1, fmt)
				date2 = datetime.datetime.now()
				date2 = datetime.datetime.strftime(date2, fmt)
				datediff = frappe.utils.data.time_diff(date2, date1)
				datediff = datediff.__str__()
				#frappe.msgprint(datediff)
				total_hrs = 0.00
				hour_str = [] 
				no_of_hours = []
				no_of_days = ""
				incr = 0
				hour_str = datediff.split(",")
				if hour_str != []:
					no_of_days = str(hour_str[0])
					#msgprint(no_of_days)
					if(("days" in no_of_days) or ('day' in no_of_days)) :
						if "days" in no_of_days :
							no_of_days = float(no_of_days.replace(" days", ""))
						else:
							no_of_days = float(no_of_days.replace(" day", ""))
						no_of_days = no_of_days *24*60*60
						no_of_hours = hour_str[1].split(":")
						if no_of_hours != []:
							hrs = float(no_of_hours[0]) *60*60
							mins = float(no_of_hours[1]) *60
							secs = float(no_of_hours[2])
							total_seconds = no_of_days + hrs + mins + secs
							total_hrs = total_seconds / 3600
							#msgprint(str(total_hrs))
					else:
						no_of_hours = hour_str[0].split(":")
						if no_of_hours != []:
							hrs = float(no_of_hours[0]) *60*60
							mins = float(no_of_hours[1]) *60
							secs = float(no_of_hours[2])
							total_seconds = hrs + mins + secs
							total_hrs = total_seconds / 3600
							#msgprint(str(total_hrs))
						#frappe.msgprint(str(e[3]))
						#frappe.msgprint("Hello")
					if total_hrs >= 2 and e[3]<=3:
						rm=int(e[3])
						rm = rm +1
						incr =int(rm)
						#frappe.msgprint(str(incr))
					elif total_hrs >= 2 and e[3]>3:
						incr = e[3]
					frappe.db.set_value("Boq", e[0], "bdm_mail_time", incr)
					#frappe.msgprint("Updated")
					if total_hrs >= 2 and e[3]<=3:
						html = """<html><head></head><body><p>"""+ e[0] + """ is pending for Approval</p></body></html>"""
						acc_manager = frappe.db.get_value("Boq", self.name, 'account_manager')
						frappe.sendmail(recipients = acc_manager,
							subject=_("{0} is pending for Approvel").format(e[0]),
							message=_("""{0}""").format(html),
							reply_to= acc_manager)
					elif total_hrs >= 2 and e[3] > 3:
						html = """<html><head></head><body><p>"""+ e[0] + """ is not approved by """ +final+ """ </p></body></html>"""
						frappe.sendmail(recipients = "gopu@tablix.ae",
							subject=_("{0} is pending for Approvel").format(e[0]),
							message=_("""{0}""").format(html),
							reply_to= "gopu@tablix.ae")
					else:
						frappe.msgprint("Email is not sent")	
	
	def kam_time():
		sql="""select name , account_manager , Date_Format(kam_date_time , "%Y-%m-%d %H:%i:%s") As date, kam_mail_time from tabBoq where status = 'KAM Approved'"""
		var=frappe.db.sql(sql)
		#frappe.msgprint(str(var))
		for e in var:
			if e[2] is not None and e[2] != "":
				nm = []
				scnd =[]
				final = ""
				name = ""
				nm = e[1].split("@")
				if nm != []:
					name = str(nm[0])
					if "." in name:
						scnd = name.split(".")
						final = str(scnd[0])
					else:
						final = name
				fmt = '%Y-%m-%d %H:%M:%S'
				date1 = datetime.datetime.strptime(e[2], fmt)
				date1 = datetime.datetime.strftime(date1, fmt)
				date2 = datetime.datetime.now()
				date2 = datetime.datetime.strftime(date2, fmt)
				datediff = frappe.utils.data.time_diff(date2, date1)
				datediff = datediff.__str__()
				#frappe.msgprint(datediff)
				total_hrs = 0.00
				hour_str = [] 
				no_of_hours = []
				no_of_days = ""
				incr = 0
				hour_str = datediff.split(",")
				if hour_str != []:
					no_of_days = str(hour_str[0])
					#msgprint(no_of_days)
					if(("days" in no_of_days) or ('day' in no_of_days)) :
						if "days" in no_of_days :
							no_of_days = float(no_of_days.replace(" days", ""))
						else:
							no_of_days = float(no_of_days.replace(" day", ""))
						no_of_days = no_of_days *24*60*60
						no_of_hours = hour_str[1].split(":")
						if no_of_hours != []:
							hrs = float(no_of_hours[0]) *60*60
							mins = float(no_of_hours[1]) *60
							secs = float(no_of_hours[2])
							total_seconds = no_of_days + hrs + mins + secs
							total_hrs = total_seconds / 3600
							#msgprint(str(total_hrs))
					else:
						no_of_hours = hour_str[0].split(":")
						if no_of_hours != []:
							hrs = float(no_of_hours[0]) *60*60
							mins = float(no_of_hours[1]) *60
							secs = float(no_of_hours[2])
							total_seconds = hrs + mins + secs
							total_hrs = total_seconds / 3600
							#msgprint(str(total_hrs))
						#frappe.msgprint(str(e[3]))
						frappe.msgprint("Hello")
					if total_hrs >= 2 and e[3]<=3:
						rm=int(e[3])
						rm = rm +1
						incr =int(rm)
						#frappe.msgprint(str(incr))
					elif total_hrs >= 2 and e[3]>3:
						incr = e[3]
					frappe.db.set_value("Boq", e[0], "kam_mail_time", incr)
					if total_hrs >= 2 and e[3]<=3:
						html = """<html><head></head><body><p>"""+ e[0] + """ is pending for Approval</p></body></html>"""
						frappe.sendmail(recipients = cbdo,
							subject=_("{0} is pending for Approvel").format(e[0]),
							message=_("""{0}""").format(html),
							reply_to= cbdo)
					elif total_hrs >= 2 and e[3] > 3:
						html = """<html><head></head><body><p>"""+ e[0] + """ is not approved by """ +final+ """ </p></body></html>"""
						frappe.sendmail(recipients = "gopu@tablix.ae",
							subject=_("{0} is pending for Approvel").format(e[0]),
							message=_("""{0}""").format(html),
							reply_to= "gopu@tablix.ae")
					else:
						frappe.msgprint("Email is not sent")
					
	def cbdo_time():
		sql="""select name , account_manager , Date_Format(cbdo_date_time , "%Y-%m-%d %H:%i:%s") As date, cbdo_mail_time from tabBoq where status = 'CBDO Approved'"""
		var=frappe.db.sql(sql)
		frappe.msgprint(str(var))
		for e in var:
			if e[2] is not None and e[2] != "":
				nm = []
				scnd =[]
				final = ""
				name = ""
				nm = e[1].split("@")
				if nm != []:
					name = str(nm[0])
					if "." in name:
						scnd = name.split(".")
						final = str(scnd[0])
					else:
						final = name
				fmt = '%Y-%m-%d %H:%M:%S'
				date1 = datetime.datetime.strptime(e[2], fmt)
				date1 = datetime.datetime.strftime(date1, fmt)
				date2 = datetime.datetime.now()
				date2 = datetime.datetime.strftime(date2, fmt)
				datediff = frappe.utils.data.time_diff(date2, date1)
				datediff = datediff.__str__()
				frappe.msgprint(datediff)
				total_hrs = 0.00
				hour_str = [] 
				no_of_hours = []
				no_of_days = ""
				incr = 0
				hour_str = datediff.split(",")
				if hour_str != []:
					no_of_days = str(hour_str[0])
					msgprint(no_of_days)
					if(("days" in no_of_days) or ('day' in no_of_days)) :
						if "days" in no_of_days :
							no_of_days = float(no_of_days.replace(" days", ""))
						else:
							no_of_days = float(no_of_days.replace(" day", ""))
						no_of_days = no_of_days *24*60*60
						no_of_hours = hour_str[1].split(":")
						if no_of_hours != []:
							hrs = float(no_of_hours[0]) *60*60
							mins = float(no_of_hours[1]) *60
							secs = float(no_of_hours[2])
							total_seconds = no_of_days + hrs + mins + secs
							total_hrs = total_seconds / 3600
							msgprint(str(total_hrs))
					else:
						no_of_hours = hour_str[0].split(":")
						if no_of_hours != []:
							hrs = float(no_of_hours[0]) *60*60
							mins = float(no_of_hours[1]) *60
							secs = float(no_of_hours[2])
							total_seconds = hrs + mins + secs
							total_hrs = total_seconds / 3600
							msgprint(str(total_hrs))
					frappe.msgprint(str(e[3]))
					frappe.msgprint("Hello")
					if total_hrs >= 2 and e[3]<=3:
						rm=int(e[3])
						rm = rm +1
						incr =int(rm)
						frappe.msgprint(str(incr))
					elif total_hrs >= 2 and e[3]>3:
						incr = e[3]
					frappe.db.set_value("Boq", e[0], "cbdo_mail_time", incr)
					frappe.msgprint("Updated")
					if total_hrs >= 2 and e[3]<=3:
						html = """<html><head></head><body><p>"""+ e[0] + """ is pending for Approval</p></body></html>"""
						frappe.sendmail(recipients = finance_emp,
							subject=_("{0} is pending for Approvel").format(e[0]),
							message=_("""{0}""").format(html),
							reply_to= finance_emp)
					elif total_hrs >= 2 and e[3] > 3:
						html = """<html><head></head><body><p>"""+ e[0] + """ is not approved by """ +final+ """ </p></body></html>"""
						frappe.sendmail(recipients = "gopu@tablix.ae",
							subject=_("{0} is pending for Approvel").format(e[0]),
							message=_("""{0}""").format(html),
							reply_to= "gopu@tablix.ae")
					else:
						frappe.msgprint("Email is not sent")	
					



@frappe.whitelist()
def make_quotation(source_name, target_doc=None):
	boq = frappe.get_doc("Boq", source_name)
	frappe.db.set_value("Opportunity", boq.opportunity, "status", "Quotation")
	doclist = get_mapped_doc("Boq", source_name, {
		"Boq": {
			"doctype": "Quotation",
			"field_map": {
				"name": "boq",
				"exclusions": "assumptions",
				"material_delivery_period": "delivery_terms",
				"validity_of_proposal": "validity",
				"discount_amt": "discount_amount",
				"total_amt": "total",
				"total_cost_amt": "total_cost",
				"amc_type": "amc_type",
				"boq": "is_boq"
			}
		},
		"AMC Items": {
			"doctype": "Quotation Item",
			"field_map": {
				"parent": "boq_ref",
				"stock_uom": "stock_uom",
				"rate": "rate",
				"amount": "amount"
			}
		},
		"Boq Item": {
			"doctype": "Quotation Item",
			"field_map": {
				"parent": "boq_ref",
				"stock_uom": "stock_uom",
				"selling_price": "rate",
				"sale_amount": "total"
			}
		}
	})
	

	return doclist

	
@frappe.whitelist()	
def marginapply(boq_form, app_margin_perc):
	boq = frappe.get_doc("Boq", boq_form)
	for item in boq.items:
		item.margin_percent = app_margin_perc
	return app_margin_perc
	
	
@frappe.whitelist()
def make_quotation_new(source_name, target_doc=None):
	def set_missing_values(source, target):
		quotation = frappe.get_doc(target)

		company_currency = frappe.db.get_value("Company", quotation.company, "default_currency")
		party_account_currency = get_party_account_currency("Customer", quotation.customer,
			quotation.company) if quotation.customer else company_currency

		quotation.currency = party_account_currency or company_currency

		if company_currency == quotation.currency:
			exchange_rate = 1
		else:
			exchange_rate = get_exchange_rate(quotation.currency, company_currency)

		quotation.conversion_rate = exchange_rate

		quotation.run_method("set_missing_values")
		quotation.run_method("calculate_taxes_and_totals")

	doclist = get_mapped_doc("Boq", source_name, {
		"Boq": {
			"doctype": "Quotation",
			"field_map": {
				"name": "boq",
				"exclusions": "assumptions",
				"material_delivery_period": "delivery_terms",
				"validity_of_proposal": "validity",
				"discount_amt": "discount_amount",
				"total_amt": "total",
				"total_cost_amt": "total_cost",
				"amc_type": "amc_type",
				"boq": "is_boq"
			}
		},
		"Boq Item": {
			"doctype": "Quotation Item",
			"field_map": {
				"stock_uom": "stock_uom",
				"selling_price": "rate",
				"sale_amount": "total"
			},
		},
		"AMC Items": {
			"doctype": "Quotation Item",
			"field_map": {
				"stock_uom": "stock_uom",
				"rate": "rate",
				"amount": "amount"
			},
		}
	},target_doc, set_missing_values)
		
	return doclist
			