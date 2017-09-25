from __future__ import unicode_literals
import frappe
<<<<<<< HEAD

def execute():
	return
	# frappe.reload_doc('website', 'doctype', 'style_settings')
	# style_settings = frappe.get_doc("Style Settings", "Style Settings")
	# if not style_settings.apply_style:
	# 	style_settings.update(default_properties)
	# 	style_settings.apply_style = 1
	# 	style_settings.save()
=======
from frappe.www.style_settings import default_properties

def execute():
	frappe.reload_doc('website', 'doctype', 'style_settings')
	style_settings = frappe.get_doc("Style Settings", "Style Settings")
	if not style_settings.apply_style:
		style_settings.update(default_properties)
		style_settings.apply_style = 1
		style_settings.save()
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
