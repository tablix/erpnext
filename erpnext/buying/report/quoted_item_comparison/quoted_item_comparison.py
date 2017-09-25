# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from erpnext.setup.utils import get_exchange_rate
<<<<<<< HEAD
from frappe.utils import flt, cint
import frappe

def execute(filters=None):
=======

import frappe

def execute(filters=None):
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	qty_list = get_quantity_list(filters.item)
	
	data = get_quote_list(filters.item, qty_list)
	
	columns = get_columns(qty_list)
	
	return columns, data
<<<<<<< HEAD
	
def get_quote_list(item, qty_list):
	out = []
=======

	
def get_quote_list(item, qty_list):
	
	out = []
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	if item:
		price_data = []
		suppliers = []
		company_currency = frappe.db.get_default("currency")
<<<<<<< HEAD
		float_precision = cint(frappe.db.get_default("float_precision")) or 2 
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		# Get the list of suppliers
		for root in frappe.db.sql("""select parent, qty, rate from `tabSupplier Quotation Item` where item_code=%s and docstatus < 2""", item, as_dict=1):
			for splr in frappe.db.sql("""SELECT supplier from `tabSupplier Quotation` where name =%s and docstatus < 2""", root.parent, as_dict=1):
				ip = frappe._dict({
				"supplier": splr.supplier,
				"qty": root.qty,
				"parent": root.parent,
				"rate": root.rate})
				price_data.append(ip)
				suppliers.append(splr.supplier)
			
		#Add a row for each supplier
		for root in set(suppliers):
<<<<<<< HEAD
			supplier_currency = frappe.db.get_value("Supplier", root, "default_currency")
			if supplier_currency:
				exchange_rate = get_exchange_rate(supplier_currency, company_currency)
			else:
				exchange_rate = 1
=======
			supplier_currency = frappe.db.get_value("Supplier",root,"default_currency")
			exg = get_exchange_rate(supplier_currency,company_currency)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

			row = frappe._dict({
				"supplier_name": root
			})
			for col in qty_list:
				# Get the quantity for this row
				for item_price in price_data:
					if str(item_price.qty) == col.key and item_price.supplier == root:
<<<<<<< HEAD
						row[col.key] = flt(item_price.rate * exchange_rate, float_precision)
=======
						row[col.key] = item_price.rate * exg
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
						row[col.key + "QUOTE"] = item_price.parent
						break
					else:
						row[col.key] = ""
						row[col.key + "QUOTE"] = ""
			out.append(row)
			
<<<<<<< HEAD
	return out
	
def get_quantity_list(item):
	out = []
	
=======

	
	return out
	
def get_quantity_list(item):
	
	out = []
	
			
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	if item:
		qty_list = frappe.db.sql("""select distinct qty from `tabSupplier Quotation Item` where ifnull(item_code,'')=%s and docstatus < 2""", item, as_dict=1)
		qty_list.sort(reverse=False)
		for qt in qty_list:
			col = frappe._dict({
				"key": str(qt.qty),
				"label": "Qty: " + str(int(qt.qty))
			})
			out.append(col)

	return out
	
def get_columns(qty_list):
	columns = [{
		"fieldname": "supplier_name",
		"label": "Supplier",
		"fieldtype": "Link",
		"options": "Supplier",
		"width": 200
	}]

	for qty in qty_list:
		columns.append({
			"fieldname": qty.key,
			"label": qty.label,
			"fieldtype": "Currency",
			"options": "currency",
			"width": 80
		})
		columns.append({
			"fieldname": qty.key + "QUOTE",
			"label": "Quotation",
			"fieldtype": "Link",
			"options": "Supplier Quotation",
			"width": 90
		})

<<<<<<< HEAD
	return columns
=======

	return columns
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
