# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals

import frappe
<<<<<<< HEAD
from frappe.utils import flt, add_days, nowdate, add_months
=======
from frappe.utils import flt
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
import unittest

test_dependencies = ["Product Bundle"]

class TestQuotation(unittest.TestCase):
	def test_make_sales_order(self):
		from erpnext.selling.doctype.quotation.quotation import make_sales_order

		quotation = frappe.copy_doc(test_records[0])
<<<<<<< HEAD
		quotation.transaction_date = nowdate()
		quotation.valid_till = add_months(quotation.transaction_date, 1)
		quotation.insert()

		self.assertRaises(frappe.ValidationError, make_sales_order, quotation.name)
=======
		quotation.insert()

		self.assertRaises(frappe.ValidationError, make_sales_order, quotation.name)

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		quotation.submit()

		sales_order = make_sales_order(quotation.name)

		self.assertEquals(sales_order.doctype, "Sales Order")
		self.assertEquals(len(sales_order.get("items")), 1)
		self.assertEquals(sales_order.get("items")[0].doctype, "Sales Order Item")
		self.assertEquals(sales_order.get("items")[0].prevdoc_docname, quotation.name)
		self.assertEquals(sales_order.customer, "_Test Customer")

		sales_order.delivery_date = "2014-01-01"
		sales_order.naming_series = "_T-Quotation-"
<<<<<<< HEAD
		sales_order.transaction_date = nowdate()
		sales_order.insert()

	def test_valid_till(self):
		from erpnext.selling.doctype.quotation.quotation import make_sales_order

		quotation = frappe.copy_doc(test_records[0])
		quotation.valid_till = add_days(quotation.transaction_date, -1)
		self.assertRaises(frappe.ValidationError, quotation.validate)

		quotation.valid_till = add_days(nowdate(), -1)
		quotation.insert()
		quotation.submit()
		self.assertRaises(frappe.ValidationError, make_sales_order, quotation.name)

=======
		sales_order.transaction_date = "2013-05-12"
		sales_order.insert()

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def test_create_quotation_with_margin(self):
		from erpnext.selling.doctype.quotation.quotation import make_sales_order
		from erpnext.selling.doctype.sales_order.sales_order \
			import make_delivery_note, make_sales_invoice

<<<<<<< HEAD
		rate_with_margin = flt((1500*18.75)/100 + 1500)
=======
		total_margin = flt((1500*18.75)/100 + 1500)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

		test_records[0]['items'][0]['price_list_rate'] = 1500
		test_records[0]['items'][0]['margin_type'] = 'Percentage'
		test_records[0]['items'][0]['margin_rate_or_amount'] = 18.75

		quotation = frappe.copy_doc(test_records[0])
<<<<<<< HEAD
		quotation.transaction_date = nowdate()
		quotation.valid_till = add_months(quotation.transaction_date, 1)
		quotation.insert()

		self.assertEquals(quotation.get("items")[0].rate, rate_with_margin)
=======
		quotation.insert()

		self.assertEquals(quotation.get("items")[0].rate, total_margin)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		self.assertRaises(frappe.ValidationError, make_sales_order, quotation.name)
		quotation.submit()

		sales_order = make_sales_order(quotation.name)
<<<<<<< HEAD
		sales_order.naming_series = "_T-Quotation-"
		sales_order.transaction_date = "2016-01-01"
		sales_order.delivery_date = "2016-01-02"

		sales_order.insert()

		self.assertEquals(quotation.get("items")[0].rate, rate_with_margin)
=======
		sales_order.delivery_date = "2016-01-02"
		sales_order.naming_series = "_T-Quotation-"
		sales_order.transaction_date = "2016-01-01"
		sales_order.insert()

		self.assertEquals(quotation.get("items")[0].rate, total_margin)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

		sales_order.submit()

		dn = make_delivery_note(sales_order.name)
<<<<<<< HEAD
		self.assertEquals(quotation.get("items")[0].rate, rate_with_margin)
		dn.save()

		si = make_sales_invoice(sales_order.name)
		self.assertEquals(quotation.get("items")[0].rate, rate_with_margin)
		si.save()

	def test_create_two_quotations(self):
		from erpnext.stock.doctype.item.test_item import make_item

		first_item = make_item("_Test Laptop",
							{"is_stock_item": 1, "expense_account": "_Test Account Cost for Goods Sold - _TC",
							 "cost_center": "_Test Cost Center - _TC"})

		second_item = make_item("_Test CPU",
							{"is_stock_item": 1, "expense_account": "_Test Account Cost for Goods Sold - _TC",
							 "cost_center": "_Test Cost Center - _TC"})

		qo_item1 = [
			{
				"item_code": first_item.item_code,
				"warehouse": "",
				"qty": 2,
				"rate": 400,
				"delivered_by_supplier": 1,
				"supplier": '_Test Supplier'
			}
		]

		qo_item2 = [
			{
				"item_code": second_item.item_code,
				"warehouse": "_Test Warehouse - _TC",
				"qty": 2,
				"rate": 300,
				"conversion_factor": 1.0
			}
		]

		first_qo = make_quotation(item_list=qo_item1, do_not_submit=True)
		first_qo.submit()
		sec_qo = make_quotation(item_list=qo_item2, do_not_submit=True)
		sec_qo.submit()
=======
		self.assertEquals(quotation.get("items")[0].rate, total_margin)
		dn.save()

		si = make_sales_invoice(sales_order.name)
		self.assertEquals(quotation.get("items")[0].rate, total_margin)
		si.save()

	def test_party_status_open(self):
		from erpnext.selling.doctype.customer.test_customer import get_customer_dict

		customer = frappe.get_doc(get_customer_dict('Party Status Test')).insert()
		self.assertEquals(frappe.db.get_value('Customer', customer.name, 'status'), 'Active')

		quotation = frappe.get_doc(get_quotation_dict(customer=customer.name)).insert()
		self.assertEquals(frappe.db.get_value('Customer', customer.name, 'status'), 'Open')

		quotation.submit()
		self.assertEquals(frappe.db.get_value('Customer', customer.name, 'status'), 'Active')

		quotation.cancel()
		quotation.delete()
		customer.delete()

	def test_party_status_close(self):
		from erpnext.selling.doctype.customer.test_customer import get_customer_dict

		customer = frappe.get_doc(get_customer_dict('Party Status Test')).insert()
		self.assertEquals(frappe.db.get_value('Customer', customer.name, 'status'), 'Active')

		# open quotation
		quotation = frappe.get_doc(get_quotation_dict(customer=customer.name)).insert()
		self.assertEquals(frappe.db.get_value('Customer', customer.name, 'status'), 'Open')

		# close quotation (submit)
		quotation.submit()

		quotation1 = frappe.get_doc(get_quotation_dict(customer=customer.name)).insert()

		# still open
		self.assertEquals(frappe.db.get_value('Customer', customer.name, 'status'), 'Open')

		quotation.cancel()
		quotation.delete()

		quotation1.delete()

		customer.delete()
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

test_records = frappe.get_test_records('Quotation')

def get_quotation_dict(customer=None, item_code=None):
	if not customer:
		customer = '_Test Customer'
	if not item_code:
		item_code = '_Test Item'

	return {
		'doctype': 'Quotation',
		'customer': customer,
		'items': [
			{
				'item_code': item_code,
				'qty': 1,
				'rate': 100
			}
		]
<<<<<<< HEAD
	}


def make_quotation(**args):
	qo = frappe.new_doc("Quotation")
	args = frappe._dict(args)
	if args.transaction_date:
		qo.transaction_date = args.transaction_date

	qo.company = args.company or "_Test Company"
	qo.customer = args.customer or "_Test Customer"
	qo.currency = args.currency or "INR"
	if args.selling_price_list:
		qo.selling_price_list = args.selling_price_list

	if "warehouse" not in args:
		args.warehouse = "_Test Warehouse - _TC"

	if args.item_list:
		for item in args.item_list:
			qo.append("items", item)

	else:
		qo.append("items", {
			"item_code": args.item or args.item_code or "_Test Item",
			"warehouse": args.warehouse,
			"qty": args.qty or 10,
			"uom": args.uom or None,
			"rate": args.rate or 100
		})

	qo.delivery_date = add_days(qo.transaction_date, 10)

	if not args.do_not_save:
		qo.insert()
		if not args.do_not_submit:
			qo.submit()

	return qo
=======
	}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
