# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ProductionOrderItem(Document):
	pass
<<<<<<< HEAD

def on_doctype_update():
	frappe.db.add_index("Production Order Item", ["item_code", "source_warehouse"])
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
