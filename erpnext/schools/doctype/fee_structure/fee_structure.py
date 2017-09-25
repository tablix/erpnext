# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
<<<<<<< HEAD
from frappe.model.mapper import get_mapped_doc

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

class FeeStructure(Document):
	def validate(self):
		self.calculate_total()
		
	def calculate_total(self):
		"""Calculates total amount."""
		self.total_amount = 0
		for d in self.components:
			self.total_amount += d.amount
	
<<<<<<< HEAD

@frappe.whitelist()
def make_fee_schedule(source_name, target_doc=None):
	return get_mapped_doc("Fee Structure", source_name,	{
		"Fee Structure": {
			"doctype": "Fee Schedule",
			"validation": {
				"docstatus": ["=", 1],
			}
		},
		"Fee Component": {
			"doctype": "Fee Component"
		}
	}, target_doc)
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
