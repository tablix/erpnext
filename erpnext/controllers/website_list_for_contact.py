# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import json
import frappe
from frappe import _
<<<<<<< HEAD
from frappe.utils import flt, has_common
=======
from frappe.utils import flt
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
from frappe.utils.user import is_website_user

def get_list_context(context=None):
	return {
		"global_number_format": frappe.db.get_default("number_format") or "#,###.##",
		"currency": frappe.db.get_default("currency"),
		"currency_symbols": json.dumps(dict(frappe.db.sql("""select name, symbol
			from tabCurrency where enabled=1"""))),
		"row_template": "templates/includes/transaction_row.html",
		"get_list": get_transaction_list
	}

<<<<<<< HEAD

def get_transaction_list(doctype, txt=None, filters=None, limit_start=0, limit_page_length=20, order_by="modified"):
=======
def get_transaction_list(doctype, txt=None, filters=None, limit_start=0, limit_page_length=20):
	from frappe.www.list import get_list
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	user = frappe.session.user
	key = None

	if not filters: filters = []

<<<<<<< HEAD
	if doctype == 'Supplier Quotation':
		filters.append((doctype, "docstatus", "<", 2))
	else:
		filters.append((doctype, "docstatus", "=", 1))

	if (user != "Guest" and is_website_user()) or doctype == 'Request for Quotation':
=======
	filters.append((doctype, "docstatus", "=", 1))

	if user != "Guest" and is_website_user():
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		parties_doctype = 'Request for Quotation Supplier' if doctype == 'Request for Quotation' else doctype
		# find party for this contact
		customers, suppliers = get_customers_suppliers(parties_doctype, user)

		if not customers and not suppliers: return []

		key, parties = get_party_details(customers, suppliers)

		if doctype == 'Request for Quotation':
			return rfq_transaction_list(parties_doctype, doctype, parties, limit_start, limit_page_length)

		filters.append((doctype, key, "in", parties))

		if key:
<<<<<<< HEAD
			return post_process(doctype, get_list_for_transactions(doctype, txt,
				filters=filters, fields="name",limit_start=limit_start,
				limit_page_length=limit_page_length,ignore_permissions=True,
				order_by="modified desc"))
		else:
			return []

	return post_process(doctype, get_list_for_transactions(doctype, txt, filters, limit_start, limit_page_length,
		fields="name", order_by="modified desc"))

def get_list_for_transactions(doctype, txt, filters, limit_start, limit_page_length=20,
	ignore_permissions=False,fields=None, order_by=None):
	""" Get List of transactions like Invoices, Orders """
	from frappe.www.list import get_list
	meta = frappe.get_meta(doctype)
	data = []
	or_filters = []

	for d in get_list(doctype, txt, filters=filters, fields="name", limit_start=limit_start,
		limit_page_length=limit_page_length, ignore_permissions=ignore_permissions, order_by="modified desc"):
		data.append(d)

	if txt:
		if meta.get_field('items'):
			if meta.get_field('items').options:
				child_doctype = meta.get_field('items').options
				for item in frappe.get_all(child_doctype, {"item_name": ['like', "%" + txt + "%"]}):
					child = frappe.get_doc(child_doctype, item.name)
					or_filters.append([doctype, "name", "=", child.parent])

	if or_filters:
		for r in frappe.get_list(doctype, fields=fields,filters=filters, or_filters=or_filters,
			limit_start=limit_start, limit_page_length=limit_page_length, 
			ignore_permissions=ignore_permissions, order_by=order_by):
			data.append(r)

	return data
=======
			return post_process(doctype, get_list(doctype, txt,
				filters=filters, fields = "name",
				limit_start=limit_start, limit_page_length=limit_page_length,
				ignore_permissions=True,
				order_by = "modified desc"))
		else:
			return []

	return post_process(doctype, get_list(doctype, txt, filters, limit_start, limit_page_length,
		fields="name", order_by = "modified desc"))
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

def get_party_details(customers, suppliers):
	if customers:
		key, parties = "customer", customers
	elif suppliers:
		key, parties = "supplier", suppliers
	else:
		key, parties = "customer", []

	return key, parties

def rfq_transaction_list(parties_doctype, doctype, parties, limit_start, limit_page_length):
	data = frappe.db.sql("""select distinct parent as name, supplier from `tab{doctype}`
			where supplier = '{supplier}' and docstatus=1  order by modified desc limit {start}, {len}""".
			format(doctype=parties_doctype, supplier=parties[0], start=limit_start, len = limit_page_length), as_dict=1)

	return post_process(doctype, data)

def post_process(doctype, data):
	result = []
	for d in data:
		doc = frappe.get_doc(doctype, d.name)

		doc.status_percent = 0
		doc.status_display = []

		if doc.get("per_billed"):
			doc.status_percent += flt(doc.per_billed)
			doc.status_display.append(_("Billed") if doc.per_billed==100 else _("{0}% Billed").format(doc.per_billed))

		if doc.get("per_delivered"):
			doc.status_percent += flt(doc.per_delivered)
			doc.status_display.append(_("Delivered") if doc.per_delivered==100 else _("{0}% Delivered").format(doc.per_delivered))

		if hasattr(doc, "set_indicator"):
			doc.set_indicator()

		doc.status_display = ", ".join(doc.status_display)
		doc.items_preview = ", ".join([d.item_name for d in doc.items if d.item_name])
		result.append(doc)

	return result

def get_customers_suppliers(doctype, user):
<<<<<<< HEAD
	customers = []
	suppliers = []
	meta = frappe.get_meta(doctype)

	if has_common(["Supplier", "Customer"], frappe.get_roles(user)):
		contacts = frappe.db.sql("""
			select 
				`tabContact`.email_id,
				`tabDynamic Link`.link_doctype,
				`tabDynamic Link`.link_name
			from 
				`tabContact`, `tabDynamic Link`
			where
				`tabContact`.name=`tabDynamic Link`.parent and `tabContact`.email_id =%s
			""", user, as_dict=1)
		customers = [c.link_name for c in contacts if c.link_doctype == 'Customer'] \
			if meta.get_field("customer") else None
		suppliers = [c.link_name for c in contacts if c.link_doctype == 'Supplier'] \
			if meta.get_field("supplier") else None
	elif frappe.has_permission(doctype, 'read', user=user):
		customers = [customer.name for customer in frappe.get_list("Customer")] \
			if meta.get_field("customer") else None
		suppliers = [supplier.name for supplier in frappe.get_list("Customer")] \
			if meta.get_field("supplier") else None
=======
	meta = frappe.get_meta(doctype)
	contacts = frappe.get_all("Contact", fields=["customer", "supplier", "email_id"],
		filters={"email_id": user})

	customers = [c.customer for c in contacts if c.customer] if meta.get_field("customer") else None
	suppliers = [c.supplier for c in contacts if c.supplier] if meta.get_field("supplier") else None
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	return customers, suppliers

def has_website_permission(doc, ptype, user, verbose=False):
	doctype = doc.doctype
	customers, suppliers = get_customers_suppliers(doctype, user)
	if customers:
		return frappe.get_all(doctype, filters=[(doctype, "customer", "in", customers),
			(doctype, "name", "=", doc.name)]) and True or False
	elif suppliers:
<<<<<<< HEAD
		fieldname = 'suppliers' if doctype == 'Request for Quotation' else 'supplier'
		return frappe.get_all(doctype, filters=[(doctype, fieldname, "in", suppliers),
=======
		return frappe.get_all(doctype, filters=[(doctype, "suppliers", "in", suppliers),
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			(doctype, "name", "=", doc.name)]) and True or False
	else:
		return False
