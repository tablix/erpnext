# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from frappe.model.document import Document

class BuyingSettings(Document):
<<<<<<< HEAD
=======
		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def validate(self):
		for key in ["supplier_type", "supp_master_name", "maintain_same_rate", "buying_price_list"]:
			frappe.db.set_default(key, self.get(key, ""))

		from erpnext.setup.doctype.naming_series.naming_series import set_by_naming_series
<<<<<<< HEAD
		set_by_naming_series("Supplier", "supplier_name",
=======
		set_by_naming_series("Supplier", "supplier_name", 
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			self.get("supp_master_name")=="Naming Series", hide_name_field=False)
