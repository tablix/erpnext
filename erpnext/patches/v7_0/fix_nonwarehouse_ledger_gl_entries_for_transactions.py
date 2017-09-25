# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

<<<<<<< HEAD
from __future__ import print_function, unicode_literals
import frappe, erpnext

def execute():
	frappe.reload_doctype("Account")

	warehouses = frappe.db.sql("""select name, company from tabAccount
		where account_type = 'Stock' and is_group = 0
		and (warehouse is null or warehouse = '')""", as_dict=1)
	warehouses = [d.name for d in warehouses if erpnext.is_perpetual_inventory_enabled(d.company)]

	if len(warehouses) > 0:
=======
from __future__ import unicode_literals
import frappe

def execute():
	if not frappe.db.get_single_value("Accounts Settings", "auto_accounting_for_stock"):
		return
	
	frappe.reload_doctype("Account")

	warehouses = frappe.db.sql_list("""select name from tabAccount
		where account_type = 'Stock' and is_group = 0
		and (warehouse is null or warehouse = '')""")
	if warehouses:
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		warehouses = set_warehouse_for_stock_account(warehouses)
		if not warehouses:
			return

		stock_vouchers = frappe.db.sql("""select distinct sle.voucher_type, sle.voucher_no
			from `tabStock Ledger Entry` sle
			where sle.warehouse in (%s) and creation > '2016-05-01'
			and not exists(select name from `tabGL Entry` 
				where account=sle.warehouse and voucher_type=sle.voucher_type and voucher_no=sle.voucher_no)
			order by sle.posting_date""" %
			', '.join(['%s']*len(warehouses)), tuple(warehouses))

		rejected = []
		for voucher_type, voucher_no in stock_vouchers:
			try:
				frappe.db.sql("""delete from `tabGL Entry`
					where voucher_type=%s and voucher_no=%s""", (voucher_type, voucher_no))

				voucher = frappe.get_doc(voucher_type, voucher_no)
				voucher.make_gl_entries()
				frappe.db.commit()
<<<<<<< HEAD
			except Exception as e:
				print(frappe.get_traceback())
				rejected.append([voucher_type, voucher_no])
				frappe.db.rollback()

		print(rejected)
=======
			except Exception, e:
				print frappe.get_traceback()
				rejected.append([voucher_type, voucher_no])
				frappe.db.rollback()

		print rejected
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

def set_warehouse_for_stock_account(warehouse_account):
	for account in warehouse_account:
		if frappe.db.exists('Warehouse', account):
			frappe.db.set_value("Account", account, "warehouse", account)
		else:
			warehouse_account.remove(account)

	return warehouse_account
