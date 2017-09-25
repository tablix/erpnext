import frappe
import erpnext.setup.install

def execute():
<<<<<<< HEAD
	frappe.reload_doc("website", "doctype", "web_form_field", force=True, reset_permissions=True)
=======
	frappe.reload_doc("website", "doctype", "web_form_field", force=True)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	#erpnext.setup.install.add_web_forms()
