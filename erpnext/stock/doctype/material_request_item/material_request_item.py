# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from frappe.model.document import Document

class MaterialRequestItem(Document):
<<<<<<< HEAD
	pass

def on_doctype_update():
	frappe.db.add_index("Material Request Item", ["item_code", "warehouse"])
=======
	pass
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
