<<<<<<< HEAD
from __future__ import print_function
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
import frappe

def execute():
	frappe.reload_doctype("File")
	frappe.reload_doctype("Item")
	for item in frappe.get_all("Item", fields=("name", "website_image", "thumbnail")):
		if item.website_image and not item.thumbnail:
			item_doc = frappe.get_doc("Item", item.name)
			try:
				item_doc.make_thumbnail()
				if item_doc.thumbnail:
					item_doc.db_set("thumbnail", item_doc.thumbnail, update_modified=False)
			except Exception:
<<<<<<< HEAD
				print("Unable to make thumbnail for {0}".format(item.website_image.encode("utf-8")))
=======
				print "Unable to make thumbnail for {0}".format(item.website_image.encode("utf-8"))
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
