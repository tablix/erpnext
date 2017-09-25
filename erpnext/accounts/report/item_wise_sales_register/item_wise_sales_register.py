# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
<<<<<<< HEAD
import frappe, erpnext
from frappe import _
from frappe.utils import flt
from frappe.model.meta import get_field_precision
from erpnext.accounts.report.sales_register.sales_register import get_mode_of_payments

def execute(filters=None):
	return _execute(filters)

def _execute(filters=None, additional_table_columns=None, additional_query_columns=None):
	if not filters: filters = {}
	columns = get_columns(additional_table_columns)

	company_currency = erpnext.get_company_currency(filters.company)

	item_list = get_items(filters, additional_query_columns)
	if item_list:
		itemised_tax, tax_columns = get_tax_accounts(item_list, columns, company_currency)
=======
import frappe
from frappe import _
from frappe.utils import flt
from erpnext.accounts.report.sales_register.sales_register import get_mode_of_payments

def execute(filters=None):
	if not filters: filters = {}
	columns = get_columns()
	last_col = len(columns)

	item_list = get_items(filters)
	if item_list:
		item_row_tax, tax_accounts = get_tax_accounts(item_list, columns)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	columns.append({
		"fieldname": "currency",
		"label": _("Currency"),
		"fieldtype": "Data",
		"width": 80
	})
<<<<<<< HEAD
	mode_of_payments = get_mode_of_payments(set([d.parent for d in item_list]))
	so_dn_map = get_delivery_notes_against_sales_order(item_list)
=======
	company_currency = frappe.db.get_value("Company", filters.company, "default_currency")
	mode_of_payments = get_mode_of_payments(set([d.parent for d in item_list]))
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	data = []
	for d in item_list:
		delivery_note = None
		if d.delivery_note:
			delivery_note = d.delivery_note
		elif d.so_detail:
<<<<<<< HEAD
			delivery_note = ", ".join(so_dn_map.get(d.so_detail, []))

		if not delivery_note and d.update_stock:
			delivery_note = d.parent

		row = [d.item_code, d.item_name, d.item_group, d.parent, d.posting_date, d.customer, d.customer_name]

		if additional_query_columns:
			for col in additional_query_columns:
				row.append(d.get(col))

		row += [
			d.customer_group, d.debit_to, ", ".join(mode_of_payments.get(d.parent, [])),
			d.territory, d.project, d.company, d.sales_order,
			delivery_note, d.income_account, d.cost_center, d.stock_qty, d.stock_uom,
			d.base_net_rate, d.base_net_amount
		]

		total_tax = 0
		for tax in tax_columns:
			item_tax = itemised_tax.get(d.name, {}).get(tax, {})
			row += [item_tax.get("tax_rate", 0), item_tax.get("tax_amount", 0)]
			total_tax += flt(item_tax.get("tax_amount"))

=======
			delivery_note = ", ".join(frappe.db.sql_list("""select distinct parent
			from `tabDelivery Note Item` where docstatus=1 and so_detail=%s""", d.so_detail))

		row = [d.item_code, d.item_name, d.item_group, d.parent, d.posting_date, d.customer, d.customer_name,
			d.customer_group, d.debit_to, ", ".join(mode_of_payments.get(d.parent, [])), 
			d.territory, d.project, d.company, d.sales_order,
			delivery_note, d.income_account, d.cost_center, d.qty, d.base_net_rate, d.base_net_amount]

		for tax in tax_accounts:
			row.append(item_row_tax.get(d.name, {}).get(tax, 0))

		total_tax = sum(row[last_col:])
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		row += [total_tax, d.base_net_amount + total_tax, company_currency]

		data.append(row)

	return columns, data

<<<<<<< HEAD
def get_columns(additional_table_columns):
	columns = [
		_("Item Code") + ":Link/Item:120", _("Item Name") + "::120",
		_("Item Group") + ":Link/Item Group:100", _("Invoice") + ":Link/Sales Invoice:120",
		_("Posting Date") + ":Date:80", _("Customer") + ":Link/Customer:120",
		_("Customer Name") + "::120"]

	if additional_table_columns:
		columns += additional_table_columns

	columns += [
		_("Customer Group") + ":Link/Customer Group:120",
=======
def get_columns():
	return [
		_("Item Code") + ":Link/Item:120", _("Item Name") + "::120",
		_("Item Group") + ":Link/Item Group:100", _("Invoice") + ":Link/Sales Invoice:120",
		_("Posting Date") + ":Date:80", _("Customer") + ":Link/Customer:120",
		_("Customer Name") + "::120", _("Customer Group") + ":Link/Customer Group:120",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		_("Receivable Account") + ":Link/Account:120",
		_("Mode of Payment") + "::120", _("Territory") + ":Link/Territory:80",
		_("Project") + ":Link/Project:80", _("Company") + ":Link/Company:100",
		_("Sales Order") + ":Link/Sales Order:100", _("Delivery Note") + ":Link/Delivery Note:100",
		_("Income Account") + ":Link/Account:140", _("Cost Center") + ":Link/Cost Center:140",
<<<<<<< HEAD
		_("Stock Qty") + ":Float:120", _("Stock UOM") + "::100",
=======
		_("Qty") + ":Float:120",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		_("Rate") + ":Currency/currency:120",
		_("Amount") + ":Currency/currency:120"
	]

<<<<<<< HEAD
	return columns

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
def get_conditions(filters):
	conditions = ""

	for opts in (("company", " and company=%(company)s"),
<<<<<<< HEAD
		("customer", " and `tabSales Invoice`.customer = %(customer)s"),
		("item_code", " and `tabSales Invoice Item`.item_code = %(item_code)s"),
		("from_date", " and `tabSales Invoice`.posting_date>=%(from_date)s"),
		("to_date", " and `tabSales Invoice`.posting_date<=%(to_date)s")):
			if filters.get(opts[0]):
				conditions += opts[1]

	if filters.get("mode_of_payment"):
		conditions += """ and exists(select name from `tabSales Invoice Payment`
			where parent=si.name
				and ifnull(`tabSales Invoice Payment`.mode_of_payment, '') = %(mode_of_payment)s)"""

	return conditions

def get_items(filters, additional_query_columns):
	conditions = get_conditions(filters)
	match_conditions = frappe.build_match_conditions("Sales Invoice")
	
	if match_conditions:
		match_conditions = " and {0} ".format(match_conditions)
	
	if additional_query_columns:
		additional_query_columns = ', ' + ', '.join(additional_query_columns)

	return frappe.db.sql("""
		select
			`tabSales Invoice Item`.name, `tabSales Invoice Item`.parent,
			`tabSales Invoice`.posting_date, `tabSales Invoice`.debit_to,
			`tabSales Invoice`.project, `tabSales Invoice`.customer, `tabSales Invoice`.remarks,
			`tabSales Invoice`.territory, `tabSales Invoice`.company, `tabSales Invoice`.base_net_total,
			`tabSales Invoice Item`.item_code, `tabSales Invoice Item`.item_name,
			`tabSales Invoice Item`.item_group, `tabSales Invoice Item`.sales_order,
			`tabSales Invoice Item`.delivery_note, `tabSales Invoice Item`.income_account,
			`tabSales Invoice Item`.cost_center, `tabSales Invoice Item`.stock_qty,
			`tabSales Invoice Item`.stock_uom, `tabSales Invoice Item`.base_net_rate,
			`tabSales Invoice Item`.base_net_amount, `tabSales Invoice`.customer_name,
			`tabSales Invoice`.customer_group, `tabSales Invoice Item`.so_detail,
			`tabSales Invoice`.update_stock {0}
		from `tabSales Invoice`, `tabSales Invoice Item`
		where `tabSales Invoice`.name = `tabSales Invoice Item`.parent
			and `tabSales Invoice`.docstatus = 1 %s %s
		order by `tabSales Invoice`.posting_date desc, `tabSales Invoice Item`.item_code desc
		""".format(additional_query_columns or '') % (conditions, match_conditions), filters, as_dict=1)

def get_delivery_notes_against_sales_order(item_list):
	so_dn_map = frappe._dict()
	so_item_rows = list(set([d.so_detail for d in item_list]))

	if so_item_rows:
		delivery_notes = frappe.db.sql("""
			select parent, so_detail
			from `tabDelivery Note Item`
			where docstatus=1 and so_detail in (%s)
			group by so_detail, parent
		""" % (', '.join(['%s']*len(so_item_rows))), tuple(so_item_rows), as_dict=1)

		for dn in delivery_notes:
			so_dn_map.setdefault(dn.so_detail, []).append(dn.parent)

	return so_dn_map

def get_tax_accounts(item_list, columns, company_currency,
		doctype="Sales Invoice", tax_doctype="Sales Taxes and Charges"):
	import json
	item_row_map = {}
	tax_columns = []
	invoice_item_row = {}
	itemised_tax = {}

	tax_amount_precision = get_field_precision(frappe.get_meta(tax_doctype).get_field("tax_amount"),
		currency=company_currency) or 2

=======
		("customer", " and si.customer = %(customer)s"),
		("item_code", " and si_item.item_code = %(item_code)s"),
		("from_date", " and si.posting_date>=%(from_date)s"),
		("to_date", " and si.posting_date<=%(to_date)s")):
			if filters.get(opts[0]):
				conditions += opts[1]
				
	if filters.get("mode_of_payment"):
		conditions += """ and exists(select name from `tabSales Invoice Payment`
			 where parent=si.name 
			 	and ifnull(`tabSales Invoice Payment`.mode_of_payment, '') = %(mode_of_payment)s)"""

	return conditions

def get_items(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		select
			si_item.name, si_item.parent, si.posting_date, si.debit_to, si.project,
			si.customer, si.remarks, si.territory, si.company, si.base_net_total,
			si_item.item_code, si_item.item_name, si_item.item_group, si_item.sales_order,
			si_item.delivery_note, si_item.income_account, si_item.cost_center, si_item.qty,
			si_item.base_net_rate, si_item.base_net_amount, si.customer_name,
			si.customer_group, si_item.so_detail
		from `tabSales Invoice` si, `tabSales Invoice Item` si_item
		where si.name = si_item.parent and si.docstatus = 1 %s
		order by si.posting_date desc, si_item.item_code desc""" % conditions, filters, as_dict=1)

def get_tax_accounts(item_list, columns):
	import json
	item_row_tax = {}
	tax_accounts = []
	invoice_item_row = {}
	item_row_map = {}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	for d in item_list:
		invoice_item_row.setdefault(d.parent, []).append(d)
		item_row_map.setdefault(d.parent, {}).setdefault(d.item_code, []).append(d)

<<<<<<< HEAD
	conditions = ""
	if doctype == "Purchase Invoice":
		conditions = " and category in ('Total', 'Valuation and Total')"

	tax_details = frappe.db.sql("""
		select
			parent, description, item_wise_tax_detail,
			charge_type, base_tax_amount_after_discount_amount
		from `tab%s`
		where
			parenttype = %s and docstatus = 1
			and (description is not null and description != '')
			and parent in (%s)
			%s
		order by description
	""" % (tax_doctype, '%s', ', '.join(['%s']*len(invoice_item_row)), conditions),
		tuple([doctype] + invoice_item_row.keys()))

	for parent, description, item_wise_tax_detail, charge_type, tax_amount in tax_details:
		if description not in tax_columns and tax_amount:
			tax_columns.append(description)
=======
	tax_details = frappe.db.sql("""
		select
			parent, account_head, item_wise_tax_detail,
			charge_type, base_tax_amount_after_discount_amount
		from `tabSales Taxes and Charges`
		where
			parenttype = 'Sales Invoice' and docstatus = 1
			and (account_head is not null and account_head != '')
			and parent in (%s)
	""" % ', '.join(['%s']*len(invoice_item_row)), tuple(invoice_item_row.keys()))

	for parent, account_head, item_wise_tax_detail, charge_type, tax_amount in tax_details:
		if account_head not in tax_accounts:
			tax_accounts.append(account_head)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

		if item_wise_tax_detail:
			try:
				item_wise_tax_detail = json.loads(item_wise_tax_detail)

<<<<<<< HEAD
				for item_code, tax_data in item_wise_tax_detail.items():
					itemised_tax.setdefault(item_code, frappe._dict())

					if isinstance(tax_data, list):
						tax_rate, tax_amount = tax_data
					else:
						tax_rate = tax_data
						tax_amount = 0

					if charge_type == "Actual" and not tax_rate:
						tax_rate = "NA"
=======
				for item_code, tax_amount in item_wise_tax_detail.items():
					tax_amount = flt(tax_amount[1]) if isinstance(tax_amount, list) else flt(tax_amount)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

					item_net_amount = sum([flt(d.base_net_amount)
						for d in item_row_map.get(parent, {}).get(item_code, [])])

					for d in item_row_map.get(parent, {}).get(item_code, []):
<<<<<<< HEAD
						item_tax_amount = flt((tax_amount * d.base_net_amount) / item_net_amount) \
							if item_net_amount else 0
						if item_tax_amount:
							itemised_tax.setdefault(d.name, {})[description] = frappe._dict({
								"tax_rate": tax_rate,
								"tax_amount": flt(item_tax_amount, tax_amount_precision)
							})
=======
						item_tax_amount = flt((tax_amount * d.base_net_amount) / item_net_amount) if item_net_amount else 0
						item_row_tax.setdefault(d.name, {})[account_head] = item_tax_amount
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

			except ValueError:
				continue
		elif charge_type == "Actual" and tax_amount:
			for d in invoice_item_row.get(parent, []):
<<<<<<< HEAD
				itemised_tax.setdefault(d.name, {})[description] = frappe._dict({
					"tax_rate": "NA",
					"tax_amount": flt((tax_amount * d.base_net_amount) / d.base_net_total,
						tax_amount_precision)
				})

	tax_columns.sort()
	for desc in tax_columns:
		columns.append(desc + " Rate:Data:80")
		columns.append(desc + " Amount:Currency/currency:100")

	columns += ["Total Tax:Currency/currency:80", "Total:Currency/currency:100"]

	return itemised_tax, tax_columns
=======
				item_row_tax.setdefault(d.name, {})[account_head] = \
					flt((tax_amount * d.base_net_amount) / d.base_net_total)

	tax_accounts.sort()
	columns += [account_head + ":Currency/currency:80" for account_head in tax_accounts]
	columns += ["Total Tax:Currency/currency:80", "Total:Currency/currency:80"]

	return item_row_tax, tax_accounts
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
