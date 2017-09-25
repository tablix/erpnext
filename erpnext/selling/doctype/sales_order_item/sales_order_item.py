# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

from frappe.model.document import Document
from erpnext.controllers.print_settings import print_settings_for_item_table

class SalesOrderItem(Document):
	def __setup__(self):
		print_settings_for_item_table(self)
<<<<<<< HEAD

def on_doctype_update():
	frappe.db.add_index("Sales Order Item", ["item_code", "warehouse"])
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
