# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import json
import frappe.utils
<<<<<<< HEAD
from frappe.utils import cstr, flt, getdate, comma_and, cint
from frappe import _
from frappe.model.utils import get_fetch_values
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.stock_balance import update_bin_qty, get_reserved_qty
from frappe.desk.notifications import clear_doctype_notifications
from frappe.contacts.doctype.address.address import get_company_address
from erpnext.controllers.selling_controller import SellingController
from erpnext.accounts.doctype.subscription.subscription import get_next_schedule_date
=======
from frappe.utils import cstr, flt, getdate, comma_and, cint, get_link_to_form, money_in_words
from frappe import _, msgprint
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.stock_balance import update_bin_qty, get_reserved_qty
from frappe.desk.notifications import clear_doctype_notifications
from erpnext.controllers.recurring_document import month_map, get_next_date
from frappe.desk.form import assign_to
from erpnext.controllers.selling_controller import SellingController
import time
import datetime
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

form_grid_templates = {
	"items": "templates/form_grid/item_grid.html"
}

class WarehouseRequired(frappe.ValidationError): pass

class SalesOrder(SellingController):
	def __init__(self, arg1, arg2=None):
		super(SalesOrder, self).__init__(arg1, arg2)

	def validate(self):
		super(SalesOrder, self).validate()

		self.validate_order_type()
		self.validate_delivery_date()
<<<<<<< HEAD
		self.validate_proj_cust()
		self.validate_po()
		self.validate_uom_is_integer("stock_uom", "stock_qty")
		self.validate_uom_is_integer("uom", "qty")
		self.validate_for_items()
		self.validate_warehouse()
		self.validate_drop_ship()
=======
		self.validate_mandatory()
		self.validate_proj_cust()
		self.validate_po()
		self.validate_uom_is_integer("stock_uom", "qty")
		self.validate_for_items()
		self.validate_warehouse()
		self.validate_drop_ship()
		#new addition
		#if self.is_amc:
		#	self.validate_total()
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

		from erpnext.stock.doctype.packed_item.packed_item import make_packing_list
		make_packing_list(self)

		self.validate_with_previous_doc()
		self.set_status()

		if not self.billing_status: self.billing_status = 'Not Billed'
		if not self.delivery_status: self.delivery_status = 'Not Delivered'
<<<<<<< HEAD

	def validate_po(self):
		# validate p.o date v/s delivery date
		if self.po_date:
			for d in self.get("items"):
				if d.delivery_date and getdate(self.po_date) > getdate(d.delivery_date):
					frappe.throw(_("Row #{0}: Expected Delivery Date cannot be before Purchase Order Date")
						.format(d.idx))
=======
		
		#new addition
		if self.po_no_new :
			self.po_no = self.po_no_new
		
	
	#new addition
	
	def send_notification(self, reason, remark = ""):
		cbdo = "kartik@tablix.ae"
		cfo = "bhavish@tablix.ae"
		opp_mngr = "bala@tablix.ae"
		opp_mngr1 = "amit.tawde@tablix.ae"
		acc_emp1 = "manoj@tablix.ae"
		acc_emp2 = "roselyn@tablix.ae"
		coo = "satyajith.ashokan@tablix.ae"
		
		project_name = frappe.db.get_value("Sales Order", self.name, 'project_site_name')
		bdm = frappe.db.get_value("Sales Order", self.name, 'tablix_rep')
		acc_manager = frappe.db.get_value("Sales Order", self.name, 'account_manager')
		customer_name = frappe.db.get_value("Sales Order", self.name, 'customer_name')
		status = frappe.db.get_value("Sales Order", self.name, 'so_status')
		frappe.db.set_value("Sales Order", self.name, "reason", remark)
		#msgprint("Entry")
		if reason == "need_approval":
			val = 0
			if self.prev_status is not None and self.prev_status != "":
				frappe.db.set_value("Sales Order", self.name, "so_status", self.prev_status)
			if self.prev_status == "Open" or self.prev_status is None or self.prev_status == "":
				cur_date = datetime.datetime.now()
				cur_date = cur_date.strftime("%Y-%m-%d %H:%M:%S")
				frappe.db.set_value("Sales Order", self.name, "kam_date_time", cur_date)
				self.notify_employee(acc_manager, project_name, val, customer_name)
			elif self.prev_status == "KAM Approved":
				self.notify_employee(coo, project_name, val, customer_name)
			elif self.prev_status == "COO Approved":
				self.notify_employee(cbdo, project_name, val, customer_name)
			elif self.prev_status == "CBDO Approved":
				self.notify_employee(cfo, project_name, val, customer_name)
			frappe.db.set_value("Sales Order", self.name, "reason", "")
			frappe.db.set_value("Sales Order", self.name, "prev_status", "")
			frappe.db.set_value("Sales Order", self.name, "assigned", 1)
			frappe.db.commit()	
			
		elif reason == "need_info":
			if status == "Open":
				# acc_manger disapproved
				val = 1
				if bdm == "kartik@tablix.ae" or bdm == "gopu@tablix.ae":
					self.notify_employee(bdm, project_name, val, customer_name)
					bdm = "remriz.estella@tablix.ae"
				self.notify_employee(bdm, project_name, val, customer_name)
			elif status == "KAM Approved":
				# coo disapproved
				val = 10
				if bdm == "kartik@tablix.ae" or bdm == "gopu@tablix.ae":
					self.notify_employee(bdm, project_name, val, customer_name)
					bdm = "remriz.estella@tablix.ae"
				self.notify_employee(bdm, project_name, val, customer_name)
			elif status == "COO Approved":
				# cbdo disapproved
				val = 2
				if bdm == "kartik@tablix.ae" or bdm == "gopu@tablix.ae":
					self.notify_employee(bdm, project_name, val, customer_name)
					bdm = "remriz.estella@tablix.ae"
				self.notify_employee(bdm, project_name, val, customer_name)
			elif status == "CBDO Approved":
				# cfo disapproved
				val = 3
				if bdm == "kartik@tablix.ae" or bdm == "gopu@tablix.ae":
					self.notify_employee(bdm, project_name, val, customer_name)
					bdm = "remriz.estella@tablix.ae"
				self.notify_employee(bdm, project_name, val, customer_name)
			frappe.db.set_value("Sales Order", self.name, "prev_status", status)
			frappe.db.set_value("Sales Order", self.name, "so_status", "Needs Clarification")
			frappe.db.commit()
		
		elif reason == "kam_approved":
			val = 0
			if acc_manager == coo:
				self.notify_employee(cbdo, project_name, val, customer_name)
				frappe.db.set_value("Sales Order", self.name, "so_status", "COO Approved")
				cur_date=datetime.datetime.now()
				cur_date = cur_date.strftime("%Y-%m-%d %H:%M:%S")
				frappe.db.set_value("Sales Order", self.name, "cbdo_date_time", cur_date)
			else:
				self.notify_employee(coo, project_name, val, customer_name)
				frappe.db.set_value("Sales Order", self.name, "so_status", "KAM Approved")
				cur_date=datetime.datetime.now()
				cur_date = cur_date.strftime("%Y-%m-%d %H:%M:%S")
				frappe.db.set_value("Sales Order", self.name, "coo_date_time", cur_date)
			val = 4
			if bdm == "kartik@tablix.ae" or bdm == "gopu@tablix.ae":
				sales_rep = "remriz.estella@tablix.ae"
				self.notify_employee(sales_rep, project_name, val, customer_name)
			self.notify_employee(bdm, project_name, val, customer_name)
			frappe.db.set_value("Sales Order", self.name, "prev_status", "")
			
			
		elif reason == "coo_approved":
			val = 0
			if acc_manager == cbdo:
				self.notify_employee(cfo, project_name, val, customer_name)
				frappe.db.set_value("Sales Order", self.name, "so_status", "CBDO Approved")
				cur_date=datetime.datetime.now()
				cur_date = cur_date.strftime("%Y-%m-%d %H:%M:%S")
				frappe.db.set_value("Sales Order", self.name, "cfo_date_time", cur_date)
			else:
				self.notify_employee(cbdo, project_name, val, customer_name)
				frappe.db.set_value("Sales Order", self.name, "so_status", "COO Approved")
				cur_date=datetime.datetime.now()
				cur_date = cur_date.strftime("%Y-%m-%d %H:%M:%S")
				frappe.db.set_value("Sales Order", self.name, "cbdo_date_time", cur_date)
			val = 11
			if bdm == "kartik@tablix.ae" or bdm == "gopu@tablix.ae":
				sales_rep = "remriz.estella@tablix.ae"
				self.notify_employee(sales_rep, project_name, val, customer_name)
			self.notify_employee(bdm, project_name, val, customer_name)
			frappe.db.set_value("Sales Order", self.name, "prev_status", "")
			
			
		elif reason == "cbdo_approved":
			val = 0
			self.notify_employee(cfo, project_name, val, customer_name)
			val = 5
			if bdm == "kartik@tablix.ae" or bdm == "gopu@tablix.ae":
				sales_rep = "remriz.estella@tablix.ae"
				self.notify_employee(sales_rep, project_name, val, customer_name)
			self.notify_employee(bdm, project_name, val, customer_name)
			frappe.db.set_value("Sales Order", self.name, "so_status", "CBDO Approved")
			cur_date=datetime.datetime.now()
			cur_date = cur_date.strftime("%Y-%m-%d %H:%M:%S")
			frappe.db.set_value("Sales Order", self.name, "cfo_date_time", cur_date)
			frappe.db.set_value("Sales Order", self.name, "prev_status", "")
		
		elif reason == "cfo_approved":
			val = 6
			if bdm == "kartik@tablix.ae" or bdm == "gopu@tablix.ae":
				sales_rep = "remriz.estella@tablix.ae"
				self.notify_employee(sales_rep, project_name, val, customer_name)
			self.notify_employee(bdm, project_name, val, customer_name)
			frappe.db.set_value("Sales Order", self.name, "so_status", "Approved")
			if self.customer is not None:
				cust_email = frappe.db.get_value("Contact", self.contact_person, "email_id")
				#frappe.msgprint(str(cust_email))
				e = frappe.db.get_value('Employee',{'user_id' : self.tablix_rep}, ['employee_name', 'designation' , 'user_id' , 'cell_number'])
				#frappe.msgprint(str(e))
				e_name = str(e[0])
				desg = str(e[1])
				u_id = str(e[2])
				no = str(e[3])
				if no.startswith('0'):
				    no=no.replace('0','+971 ')
				if '+971' not in no and no != None:
					no = '+971 ' + no
				if e_name == None:
					e_name = ""
				if desg == None:
					desg = ""
				if u_id == None:
					u_id = ""
				if no == None:
					no = ""
				if self.po_no != None:
					html = """<html><head></head><body><p><b> Dear Client,</b><br/><br/>This is to confirm that we are in receipt of your Purchase Order reference:"""+self.po_no+""" dated: """+self.transaction_date+""" for the purchase of the said items. <br/><br/>We are thankful for the order and pleased to serve you.<br/><br/>Sincerely,<br/><br/>"""+e_name+""" <br/>"""+desg+"""<br/>"""+u_id+"""</br>"""+no+"""</p></body></html>"""
					frappe.sendmail(recipients = cust_email,
						subject=_("{0}/ Sales Order-{1}").format(self.name, self.project_site_name),
						cc = [self.tablix_rep],
						message=_("""{0}""").format(html),
						reply_to= self.tablix_rep)
				else:
					po_no ="Email Confirmation"
					html = """<html><head></head><body><p><b> Dear Client,</b><br/><br/>This is to confirm that we are in receipt of your Purchase Order reference:"""+po_no+""" dated: """+self.transaction_date+""" for the purchase of the said items. <br/><br/>We are thankful for the order and pleased to serve you.<br/><br/>Sincerely,<br/><br/>"""+e_name+""" <br/>"""+desg+"""<br/>"""+u_id+"""</br>"""+no+"""</p></body></html>"""
					frappe.sendmail(recipients = cust_email,
						subject=_("{0}/ Sales Order-{1}").format(self.name, self.project_site_name),
						cc = [self.tablix_rep],
						message=_("""{0}""").format(html),
						reply_to= self.tablix_rep)
			else:
				frappe.msgprint("not reached")
			
			frappe.db.set_value("Sales Order", self.name, "so_status", "Approved")
			frappe.db.set_value("Sales Order", self.name, "prev_status", "")
			val = 7
			self.notify_employee(opp_mngr, project_name, val, customer_name)
			self.notify_employee(opp_mngr1, project_name, val, customer_name)
			val = 8
			proj_mngr = frappe.db.get_value("Sales Order", self.name, 'manager_service_delivery')
			if proj_mngr is not None and proj_mngr != "" and proj_mngr != opp_mngr1:
				self.notify_employee(proj_mngr, project_name, val, customer_name)
			val = 9
			self.notify_employee(acc_emp1, project_name, val, customer_name)
			self.notify_employee(acc_emp2, project_name, val, customer_name)
	
		return True
	
	
	
	
	def notify_employee(self, employee, subject, val, customer):
		
		
		#msgprint("Success" + str(val))
		
		def _get_message(url=False):
			if url:
				name = get_link_to_form(self.doctype, self.name)
			else:
				name = self.name
			if val == 0:
				return (_("Sales Order")+ "- %s of %s " + _("requires Approval") + ": %s") % (subject, customer, name)
			elif val ==1:
				return (_("Sales Order")+ "- %s of %s " + _("disapproved by KAM") + ": %s") % (subject, customer, name)
			elif val == 2:
				return (_("Sales Order")+ "- %s of %s " + _("disapproved by CBDO") + ": %s") % (subject, customer, name)
			elif val == 3:
				return (_("Sales Order")+ "- %s of %s " + _("disapproved by CFO") + ": %s") % (subject, customer, name)
			elif val == 4:
				return (_("Sales Order")+ "- %s of %s " + _("approved by KAM") + ": %s") % (subject, customer, name)
			elif val == 5:
				return (_("Sales Order")+ "- %s of %s " + _("approved by CBDO") + ": %s") % (subject, customer, name)	
			elif val == 6:
				return (_("Sales Order")+ "- %s of %s " + _("approved by CFO") + ": %s") % (subject, customer, name)
			elif val == 7:
				return (_("Sales Order")+ "- %s of %s " + _("approved for Project creation") + ": %s") % (subject, customer, name)
			elif val == 8:
				return (_("Sales Order")+ "- %s of %s " + _("assigned for Project creation") + ": %s") % (subject, customer, name)
			elif val == 9:
				return (_("Sales Order")+ "- %s of %s " + _("has been newly created.") + ": %s") % (subject, customer, name)
			elif val == 10:
				return (_("Sales Order")+ "- %s of %s " + _("disapproved by COO") + ": %s") % (subject, customer, name)
			elif val == 11:
				return (_("Sales Order")+ "- %s of %s " + _("approved by COO") + ": %s") % (subject, customer, name)
		
			
		self.notify({
			# for post in messages
			"message": _get_message(url=True),
			"message_to": employee,
			"subject": _get_message(),
			"subject": _get_message(),
		})
	
		desc = ''	
		if val !=4 and val != 5 and val != 6 and val != 7 and val != 9 and val != 11:
			assign_to.clear(self.doctype, self.name)
			if val == 0:
				desc = "Sales Order Assignment for Approval"
			elif val == 1:
				desc = "Sales Order needs clarification from KAM"
			elif val == 2:
				desc = "Sales Order needs clarification from CBDO"
			elif val == 3:
				desc = "Sales Order needs clarification from CFO"
			elif val == 10:
				desc = "Sales Order needs clarification from COO"
			elif val == 8:
				desc = "Sales Order approved for Project creation"
				
			assign_to.add({
				"assign_to": employee,
				"doctype": self.doctype,
				"name": self.name,
				"description": desc
			})
	
		
		
		
	def notify(self, args):
		args = frappe._dict(args)
		from frappe.desk.page.chat.chat import post
		post(**{"txt": args.message, "contact": args.message_to, "subject": args.subject, "notify": 1})
		
	
	def validate_total(self):
		for item in self.get("items"):
			item.rate = 0.00
			item.amount = 0.00
		self.total = self.total_cost
		self.base_total = self.total * self.conversion_rate
		if self.additional_discount_percentage:
			self.discount_amount = (self.total * self.additional_discount_percentage)/100
			if self.currency != "AED":
				self.base_discount_amount = self.discount_amount * self.conversion_rate
		if self.discount_amount > 0.00:
			self.grand_total = self.total - self.discount_amount
			self.net_total = self.grand_total
		else:
			self.grand_total = self.total
			self.net_total = self.total
		self.in_words = money_in_words(self.grand_total, self.currency)	
		
		if self.currency != "AED":
			self.base_grand_total = self.grand_total * self.conversion_rate
			self.base_in_words = money_in_words(self.base_grand_total)
			self.base_rounded_total = self.base_grand_total
			self.base_net_total = self.base_grand_total
	

	def validate_mandatory(self):
		# validate transaction date v/s delivery date
		if self.delivery_date:
			if getdate(self.transaction_date) > getdate(self.delivery_date):
				frappe.throw(_("Expected Delivery Date cannot be before Sales Order Date"))

	def validate_po(self):
		# validate p.o date v/s delivery date
		if self.po_date and self.delivery_date and getdate(self.po_date) > getdate(self.delivery_date):
			frappe.throw(_("Expected Delivery Date cannot be before Purchase Order Date"))
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

		if self.po_no and self.customer:
			so = frappe.db.sql("select name from `tabSales Order` \
				where ifnull(po_no, '') = %s and name != %s and docstatus < 2\
				and customer = %s", (self.po_no, self.name, self.customer))
<<<<<<< HEAD
			if so and so[0][0] and not cint(frappe.db.get_single_value("Selling Settings",
				"allow_against_multiple_purchase_orders")):
=======
			if so and so[0][0] and not \
				cint(frappe.db.get_single_value("Selling Settings", "allow_against_multiple_purchase_orders")):
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				frappe.msgprint(_("Warning: Sales Order {0} already exists against Customer's Purchase Order {1}").format(so[0][0], self.po_no))

	def validate_for_items(self):
		check_list = []
		for d in self.get('items'):
			check_list.append(cstr(d.item_code))

			# used for production plan
			d.transaction_date = self.transaction_date

			tot_avail_qty = frappe.db.sql("select projected_qty from `tabBin` \
<<<<<<< HEAD
				where item_code = %s and warehouse = %s", (d.item_code, d.warehouse))
=======
				where item_code = %s and warehouse = %s", (d.item_code,d.warehouse))
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			d.projected_qty = tot_avail_qty and flt(tot_avail_qty[0][0]) or 0

		# check for same entry multiple times
		unique_chk_list = set(check_list)
		if len(unique_chk_list) != len(check_list) and \
			not cint(frappe.db.get_single_value("Selling Settings", "allow_multiple_items")):
<<<<<<< HEAD
			frappe.msgprint(_("Same item has been entered multiple times"),
				title=_("Warning"), indicator='orange')
=======
			frappe.msgprint(_("Warning: Same item has been entered multiple times."))
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	def product_bundle_has_stock_item(self, product_bundle):
		"""Returns true if product bundle has stock item"""
		ret = len(frappe.db.sql("""select i.name from tabItem i, `tabProduct Bundle Item` pbi
			where pbi.parent = %s and pbi.item_code = i.name and i.is_stock_item = 1""", product_bundle))
		return ret

	def validate_sales_mntc_quotation(self):
		for d in self.get('items'):
			if d.prevdoc_docname:
<<<<<<< HEAD
				res = frappe.db.sql("select name from `tabQuotation` where name=%s and order_type = %s",
					(d.prevdoc_docname, self.order_type))
				if not res:
					frappe.msgprint(_("Quotation {0} not of type {1}")
						.format(d.prevdoc_docname, self.order_type))
=======
				res = frappe.db.sql("select name from `tabQuotation` where name=%s and order_type = %s", (d.prevdoc_docname, self.order_type))
				if not res:
					frappe.msgprint(_("Quotation {0} not of type {1}").format(d.prevdoc_docname, self.order_type))
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	def validate_order_type(self):
		super(SalesOrder, self).validate_order_type()

	def validate_delivery_date(self):
<<<<<<< HEAD
		if self.order_type == 'Sales':
			if not self.delivery_date:
				self.delivery_date = max([d.delivery_date for d in self.get("items")])

			if self.delivery_date:
				for d in self.get("items"):
					if not d.delivery_date:
						d.delivery_date = self.delivery_date
					
					if getdate(self.transaction_date) > getdate(d.delivery_date):
						frappe.msgprint(_("Expected Delivery Date should be after Sales Order Date"),
							indicator='orange', title=_('Warning'))
			else:
				frappe.throw(_("Please enter Delivery Date"))
=======
		if self.order_type == 'Sales' and not self.delivery_date:
			frappe.throw(_("Please enter 'Expected Delivery Date'"))
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

		self.validate_sales_mntc_quotation()

	def validate_proj_cust(self):
		if self.project and self.customer_name:
			res = frappe.db.sql("""select name from `tabProject` where name = %s
				and (customer = %s or ifnull(customer,'')='')""",
					(self.project, self.customer))
			if not res:
				frappe.throw(_("Customer {0} does not belong to project {1}").format(self.customer, self.project))

	def validate_warehouse(self):
		super(SalesOrder, self).validate_warehouse()

		for d in self.get("items"):
<<<<<<< HEAD
			if (frappe.db.get_value("Item", d.item_code, "is_stock_item") == 1 or
=======
			if (frappe.db.get_value("Item", d.item_code, "is_stock_item")==1 or
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				(self.has_product_bundle(d.item_code) and self.product_bundle_has_stock_item(d.item_code))) \
				and not d.warehouse and not cint(d.delivered_by_supplier):
				frappe.throw(_("Delivery warehouse required for stock item {0}").format(d.item_code),
					WarehouseRequired)

	def validate_with_previous_doc(self):
		super(SalesOrder, self).validate_with_previous_doc({
			"Quotation": {
				"ref_dn_field": "prevdoc_docname",
				"compare_fields": [["company", "="], ["currency", "="]]
			}
		})


	def update_enquiry_status(self, prevdoc, flag):
		enq = frappe.db.sql("select t2.prevdoc_docname from `tabQuotation` t1, `tabQuotation Item` t2 where t2.parent = t1.name and t1.name=%s", prevdoc)
		if enq:
			frappe.db.sql("update `tabOpportunity` set status = %s where name=%s",(flag,enq[0][0]))

	def update_prevdoc_status(self, flag):
		for quotation in list(set([d.prevdoc_docname for d in self.get("items")])):
			if quotation:
				doc = frappe.get_doc("Quotation", quotation)
				if doc.docstatus==2:
					frappe.throw(_("Quotation {0} is cancelled").format(quotation))

				doc.set_status(update=True)
				doc.update_opportunity()

	def validate_drop_ship(self):
		for d in self.get('items'):
			if d.delivered_by_supplier and not d.supplier:
				frappe.throw(_("Row #{0}: Set Supplier for item {1}").format(d.idx, d.item_code))

	def on_submit(self):
<<<<<<< HEAD
=======
		#new addition
		if self.so_status != "Approved":
			frappe.throw(_("{0} cannot be submitted unless it is in Approved state").format(self.name))
		if self.po_no_new :
			self.po_no = self.po_no_new
		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		self.check_credit_limit()
		self.update_reserved_qty()

		frappe.get_doc('Authorization Control').validate_approving_authority(self.doctype, self.company, self.base_grand_total, self)
<<<<<<< HEAD
		self.update_project()
=======

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		self.update_prevdoc_status('submit')

	def on_cancel(self):
		# Cannot cancel closed SO
		if self.status == 'Closed':
			frappe.throw(_("Closed order cannot be cancelled. Unclose to cancel."))

		self.check_nextdoc_docstatus()
		self.update_reserved_qty()
<<<<<<< HEAD
		self.update_project()
=======

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		self.update_prevdoc_status('cancel')

		frappe.db.set(self, 'status', 'Cancelled')

<<<<<<< HEAD
	def update_project(self):
		project_list = []
		if self.project:
				project = frappe.get_doc("Project", self.project)
				project.flags.dont_sync_tasks = True
				project.update_sales_costing()
				project.save()
				project_list.append(self.project)

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def check_credit_limit(self):
		from erpnext.selling.doctype.customer.customer import check_credit_limit
		check_credit_limit(self.customer, self.company)

	def check_nextdoc_docstatus(self):
		# Checks Delivery Note
		submit_dn = frappe.db.sql_list("""select t1.name from `tabDelivery Note` t1,`tabDelivery Note Item` t2
			where t1.name = t2.parent and t2.against_sales_order = %s and t1.docstatus = 1""", self.name)
		if submit_dn:
			frappe.throw(_("Delivery Notes {0} must be cancelled before cancelling this Sales Order").format(comma_and(submit_dn)))

		# Checks Sales Invoice
		submit_rv = frappe.db.sql_list("""select t1.name
			from `tabSales Invoice` t1,`tabSales Invoice Item` t2
			where t1.name = t2.parent and t2.sales_order = %s and t1.docstatus = 1""",
			self.name)
		if submit_rv:
			frappe.throw(_("Sales Invoice {0} must be cancelled before cancelling this Sales Order").format(comma_and(submit_rv)))

		#check maintenance schedule
		submit_ms = frappe.db.sql_list("""select t1.name from `tabMaintenance Schedule` t1,
			`tabMaintenance Schedule Item` t2
			where t2.parent=t1.name and t2.sales_order = %s and t1.docstatus = 1""", self.name)
		if submit_ms:
			frappe.throw(_("Maintenance Schedule {0} must be cancelled before cancelling this Sales Order").format(comma_and(submit_ms)))

		# check maintenance visit
		submit_mv = frappe.db.sql_list("""select t1.name from `tabMaintenance Visit` t1, `tabMaintenance Visit Purpose` t2
			where t2.parent=t1.name and t2.prevdoc_docname = %s and t1.docstatus = 1""",self.name)
		if submit_mv:
			frappe.throw(_("Maintenance Visit {0} must be cancelled before cancelling this Sales Order").format(comma_and(submit_mv)))

		# check production order
		pro_order = frappe.db.sql_list("""select name from `tabProduction Order`
			where sales_order = %s and docstatus = 1""", self.name)
		if pro_order:
			frappe.throw(_("Production Order {0} must be cancelled before cancelling this Sales Order").format(comma_and(pro_order)))

	def check_modified_date(self):
		mod_db = frappe.db.get_value("Sales Order", self.name, "modified")
		date_diff = frappe.db.sql("select TIMEDIFF('%s', '%s')" %
			( mod_db, cstr(self.modified)))
		if date_diff and date_diff[0][0]:
			frappe.throw(_("{0} {1} has been modified. Please refresh.").format(self.doctype, self.name))

	def update_status(self, status):
		self.check_modified_date()
		self.set_status(update=True, status=status)
		self.update_reserved_qty()
		self.notify_update()
		clear_doctype_notifications(self)

	def update_reserved_qty(self, so_item_rows=None):
		"""update requested qty (before ordered_qty is updated)"""
		item_wh_list = []
		def _valid_for_reserve(item_code, warehouse):
			if item_code and warehouse and [item_code, warehouse] not in item_wh_list \
				and frappe.db.get_value("Item", item_code, "is_stock_item"):
					item_wh_list.append([item_code, warehouse])

		for d in self.get("items"):
			if (not so_item_rows or d.name in so_item_rows) and not d.delivered_by_supplier:
				if self.has_product_bundle(d.item_code):
					for p in self.get("packed_items"):
						if p.parent_detail_docname == d.name and p.parent_item == d.item_code:
							_valid_for_reserve(p.item_code, p.warehouse)
				else:
					_valid_for_reserve(d.item_code, d.warehouse)

		for item_code, warehouse in item_wh_list:
			update_bin_qty(item_code, warehouse, {
				"reserved_qty": get_reserved_qty(item_code, warehouse)
			})

	def on_update(self):
<<<<<<< HEAD
		pass

	def before_update_after_submit(self):
		self.validate_po()
		self.validate_drop_ship()
		self.validate_supplier_after_submit()
=======
		#new addition
		if self.po_no_new :
			frappe.db.set_value("Sales Order", self.name, "po_no", self.po_no_new)
			frappe.db.commit()
			
		
	
	def before_update_after_submit(self):
		#new addition
		if self.po_no_new :
			frappe.db.set_value("Sales Order", self.name, "po_no", self.po_no_new)
			frappe.db.commit()
		self.validate_drop_ship()
		self.validate_supplier_after_submit()
		#new addition
		#msgprint("Hiee")
		msd = frappe.db.get_value("Sales Order", self.name, "manager_service_delivery")
		#msgprint("MSD1:" + str(msd))
		#msgprint("MSD2:" + str(self.manager_service_delivery))
		if self.manager_service_delivery  != msd:
			#msgprint("Success !!!")
			val = 8
			project_name = self.project_site_name
			customer_name = self.customer_name
			proj_mngr = self.manager_service_delivery
			if proj_mngr is not None and proj_mngr != "":
				self.notify_employee(proj_mngr, project_name, val, customer_name)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	def validate_supplier_after_submit(self):
		"""Check that supplier is the same after submit if PO is already made"""
		exc_list = []

		for item in self.items:
			if item.supplier:
				supplier = frappe.db.get_value("Sales Order Item", {"parent": self.name, "item_code": item.item_code},
					"supplier")
				if item.ordered_qty > 0.0 and item.supplier != supplier:
					exc_list.append(_("Row #{0}: Not allowed to change Supplier as Purchase Order already exists").format(item.idx))

		if exc_list:
			frappe.throw('\n'.join(exc_list))

	def update_delivery_status(self):
		"""Update delivery status from Purchase Order for drop shipping"""
		tot_qty, delivered_qty = 0.0, 0.0

		for item in self.items:
			if item.delivered_by_supplier:
				item_delivered_qty  = frappe.db.sql("""select sum(qty)
					from `tabPurchase Order Item` poi, `tabPurchase Order` po
					where poi.sales_order_item = %s
						and poi.item_code = %s
						and poi.parent = po.name
						and po.docstatus = 1
						and po.status = 'Delivered'""", (item.name, item.item_code))

				item_delivered_qty = item_delivered_qty[0][0] if item_delivered_qty else 0
				item.db_set("delivered_qty", flt(item_delivered_qty), update_modified=False)

			delivered_qty += item.delivered_qty
			tot_qty += item.qty

		self.db_set("per_delivered", flt(delivered_qty/tot_qty) * 100,
			update_modified=False)

	def set_indicator(self):
		"""Set indicator for portal"""
		if self.per_billed < 100 and self.per_delivered < 100:
			self.indicator_color = "orange"
			self.indicator_title = _("Not Paid and Not Delivered")

		elif self.per_billed == 100 and self.per_delivered < 100:
			self.indicator_color = "orange"
			self.indicator_title = _("Paid and Not Delivered")

		else:
			self.indicator_color = "green"
			self.indicator_title = _("Paid")

<<<<<<< HEAD
	def get_production_order_items(self):
		'''Returns items with BOM that already do not have a linked production order'''
		items = []

		for table in [self.items, self.packed_items]:
			for i in table:
				bom = get_default_bom_item(i.item_code)
				if bom:
					stock_qty = i.qty if i.doctype == 'Packed Item' else i.stock_qty
					items.append(dict(
						item_code= i.item_code,
						bom = bom,
						warehouse = i.warehouse,
						pending_qty= stock_qty - flt(frappe.db.sql('''select sum(qty) from `tabProduction Order`
							where production_item=%s and sales_order=%s''', (i.item_code, self.name))[0][0])
					))

		return items

	def on_recurring(self, reference_doc, subscription_doc):
		self.set("delivery_date", get_next_schedule_date(reference_doc.delivery_date, subscription_doc.frequency,
			cint(subscription_doc.repeat_on_day)))

		for d in self.get("items"):
			reference_delivery_date = frappe.db.get_value("Sales Order Item",
				{"parent": reference_doc.name, "item_code": d.item_code, "idx": d.idx}, "delivery_date")

			d.set("delivery_date",
				get_next_schedule_date(reference_delivery_date, subscription_doc.frequency, cint(subscription_doc.repeat_on_day)))
=======
	def on_recurring(self, reference_doc):
		mcount = month_map[reference_doc.recurring_type]
		self.set("delivery_date", get_next_date(reference_doc.delivery_date, mcount,
						cint(reference_doc.repeat_on_day_of_month)))
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

def get_list_context(context=None):
	from erpnext.controllers.website_list_for_contact import get_list_context
	list_context = get_list_context(context)
	list_context.update({
		'show_sidebar': True,
		'show_search': True,
		'no_breadcrumbs': True,
		'title': _('Orders'),
	})

	return list_context
<<<<<<< HEAD
=======
	
def kam_time():
	sql="""select name , account_manager , DATE_FORMAT(kam_date_time, "%Y-%m-%d %H:%i:%s") AS date , kam_mail_sent from `tabSales Order` where so_status = 'Open' and docstatus=0"""
	var=frappe.db.sql(sql)
	#frappe.msgprint(str(var))
	for e in var:
		if e[2] is not None and e[2] != "":
			nm = []
			scnd =[]
			final = ""
			nm = e[1].split("@")
			if nm != []:
				name = str(nm[0])
				if "." in name:
					scnd = name.split(".")
					final = str(scnd[0])
				else:
					final = name
			#msgprint(e[0])
			fmt = '%Y-%m-%d %H:%M:%S' 
			date1 = datetime.datetime.strptime(e[2], fmt)
			date1 = datetime.datetime.strftime(date1, fmt)
			date2 = datetime.datetime.now()
			date2 = datetime.datetime.strftime(date2, fmt)
			datediff = frappe.utils.data.time_diff(date2, date1)
			datediff = datediff.__str__()
			#frappe.msgprint(datediff)
			total_hrs = 0.00
			hour_str = [] 
			no_of_hours = []
			no_of_days = ""
			incr = 0
			hour_str = datediff.split(",")
			if hour_str != []:
				no_of_days = str(hour_str[0])
				#msgprint(no_of_days)
				if(("days" in no_of_days) or ('day' in no_of_days)) :
					if "days" in no_of_days :
						no_of_days = float(no_of_days.replace(" days", ""))
					else:
						no_of_days = float(no_of_days.replace(" day", ""))
					no_of_days = no_of_days *24*60*60
					no_of_hours = hour_str[1].split(":")
					if no_of_hours != []:
						hrs = float(no_of_hours[0]) *60*60
						mins = float(no_of_hours[1]) *60
						secs = float(no_of_hours[2])
						total_seconds = no_of_days + hrs + mins + secs
						total_hrs = total_seconds / 3600
						#msgprint(str(total_hrs))
				else:
					no_of_hours = hour_str[0].split(":")
					if no_of_hours != []:
						hrs = float(no_of_hours[0]) *60*60
						mins = float(no_of_hours[1]) *60
						secs = float(no_of_hours[2])
						total_seconds = hrs + mins + secs
						total_hrs = total_seconds / 3600
						#msgprint(str(total_hrs))
				#frappe.msgprint(str(e[3]))
				#frappe.msgprint("Hello")
				if total_hrs >= 2 and e[3]<=3:
					rm=int(e[3])
					rm = rm +1
					incr =int(rm)
					#frappe.msgprint(str(incr))
				elif total_hrs >= 2 and e[3]>3:
					incr = e[3]
				frappe.db.set_value("Sales Order", e[0], "kam_mail_sent", incr)
				#frappe.msgprint("Updated")
				if total_hrs >= 2 and e[3]<=3:
					acc_manager = frappe.db.get_value("Sales Order", self.name, 'account_manager')
					html = """<html><head></head><body><p>"""+ e[0] + """ is pending for Approval</p></body></html>"""
					frappe.sendmail(recipients = str(acc_manager),
						subject=_("{0} is pending for Approvel").format(e[0]),
						message=_("""{0}""").format(html),
						reply_to= str(acc_manager))
				elif total_hrs >= 2 and e[3] > 3:
					html = """<html><head></head><body><p>"""+ e[0] + """ is not approved by """ +final+ """ </p></body></html>"""
					frappe.sendmail(recipients = "gopu@tablix.ae",
						subject=_("{0} is pending for Approvel").format(e[0]),
						message=_("""{0}""").format(html),
						reply_to= "gopu@tablix.ae")
				else:
					frappe.msgprint("Email is not sent heigher person")	
					
def cbdo_time():
	sql="""select name , account_manager , DATE_FORMAT(cbdo_date_time, "%Y-%m-%d %H:%i:%s") AS date , cbdo_mail_sent from `tabSales Order` where so_status = 'KAM Approved' and docstatus=0"""
	var=frappe.db.sql(sql)
	#frappe.msgprint(str(var))
	for e in var:
		if e[2] is not None and e[2] != "":
			nm = []
			scnd =[]
			final = ""
			nm = e[1].split("@")
			if nm != []:
				name = str(nm[0])
				if "." in name:
					scnd = name.split(".")
					final = str(scnd[0])
				else:
					final = name
			#msgprint(e[0])
			fmt = '%Y-%m-%d %H:%M:%S' 
			date1 = datetime.datetime.strptime(e[2], fmt)
			date1 = datetime.datetime.strftime(date1, fmt)
			date2 = datetime.datetime.now()
			date2 = datetime.datetime.strftime(date2, fmt)
			datediff = frappe.utils.data.time_diff(date2, date1)
			datediff = datediff.__str__()
			#frappe.msgprint(datediff)
			total_hrs = 0.00
			hour_str = [] 
			no_of_hours = []
			no_of_days = ""
			incr = 0
			hour_str = datediff.split(",")
			if hour_str != []:
				no_of_days = str(hour_str[0])
				#msgprint(no_of_days)
				if(("days" in no_of_days) or ('day' in no_of_days)) :
					if "days" in no_of_days :
						no_of_days = float(no_of_days.replace(" days", ""))
					else:
						no_of_days = float(no_of_days.replace(" day", ""))
					no_of_days = no_of_days *24*60*60
					no_of_hours = hour_str[1].split(":")
					if no_of_hours != []:
						hrs = float(no_of_hours[0]) *60*60
						mins = float(no_of_hours[1]) *60
						secs = float(no_of_hours[2])
						total_seconds = no_of_days + hrs + mins + secs
						total_hrs = total_seconds / 3600
						#msgprint(str(total_hrs))
				else:
					no_of_hours = hour_str[0].split(":")
					if no_of_hours != []:
						hrs = float(no_of_hours[0]) *60*60
						mins = float(no_of_hours[1]) *60
						secs = float(no_of_hours[2])
						total_seconds = hrs + mins + secs
						total_hrs = total_seconds / 3600
						#msgprint(str(total_hrs))
				#frappe.msgprint(str(e[3]))
				#frappe.msgprint("Hello")
				if total_hrs >= 2 and e[3]<=3:
					rm=int(e[3])
					rm = rm +1
					incr =int(rm)
				#	frappe.msgprint(str(incr))
				elif total_hrs >= 2 and e[3]>3:
					incr = e[3]
				frappe.db.set_value("Sales Order", e[0], "cbdo_mail_sent", incr)
				#frappe.msgprint("Updated")
				if total_hrs >= 2 and e[3]<=3:
					html = """<html><head></head><body><p>"""+ e[0] + """ is pending for Approval</p></body></html>"""
					cbdo = "kartik@tablix.ae"
					frappe.sendmail(recipients = cbdo,
						subject=_("{0} is pending for Approvel").format(e[0]),
						message=_("""{0}""").format(html),
						reply_to= cbdo)
				elif total_hrs >= 2 and e[3] > 3:
					html = """<html><head></head><body><p>"""+ e[0] + """ is not approved by """ +final+ """ </p></body></html>"""
					frappe.sendmail(recipients = "gopu@tablix.ae",
						subject=_("{0} is pending for Approvel").format(e[0]),
						message=_("""{0}""").format(html),
						reply_to= "gopu@tablix.ae")
				else:
					frappe.msgprint("Email is not sent heigher person")
def cfo_time():
	sql="""select name , account_manager , DATE_FORMAT(cfo_date_time, "%Y-%m-%d %H:%i:%s") AS date , cfo_mail_sent from `tabSales Order` where so_status = 'CBDO Approved' and docstatus=0"""
	var=frappe.db.sql(sql)
	frappe.msgprint(str(var))
	for e in var:
		if e[2] is not None and e[2] != "":
			nm = []
			scnd =[]
			final = ""
			nm = e[1].split("@")
			if nm != []:
				name = str(nm[0])
				if "." in name:
					scnd = name.split(".")
					final = str(scnd[0])
				else:
					final = name
			#msgprint(e[0])
			fmt = '%Y-%m-%d %H:%M:%S' 
			date1 = datetime.datetime.strptime(e[2], fmt)
			date1 = datetime.datetime.strftime(date1, fmt)
			date2 = datetime.datetime.now()
			date2 = datetime.datetime.strftime(date2, fmt)
			datediff = frappe.utils.data.time_diff(date2, date1)
			datediff = datediff.__str__()
			frappe.msgprint(datediff)
			total_hrs = 0.00
			hour_str = [] 
			no_of_hours = []
			no_of_days = ""
			incr = 0
			hour_str = datediff.split(",")
			if hour_str != []:
				no_of_days = str(hour_str[0])
				#msgprint(no_of_days)
				if(("days" in no_of_days) or ('day' in no_of_days)) :
					if "days" in no_of_days :
						no_of_days = float(no_of_days.replace(" days", ""))
					else:
						no_of_days = float(no_of_days.replace(" day", ""))
					no_of_days = no_of_days *24*60*60
					no_of_hours = hour_str[1].split(":")
					if no_of_hours != []:
						hrs = float(no_of_hours[0]) *60*60
						mins = float(no_of_hours[1]) *60
						secs = float(no_of_hours[2])
						total_seconds = no_of_days + hrs + mins + secs
						total_hrs = total_seconds / 3600
						msgprint(str(total_hrs))
				else:
					no_of_hours = hour_str[0].split(":")
					if no_of_hours != []:
						hrs = float(no_of_hours[0]) *60*60
						mins = float(no_of_hours[1]) *60
						secs = float(no_of_hours[2])
						total_seconds = hrs + mins + secs
						total_hrs = total_seconds / 3600
						msgprint(str(total_hrs))
				frappe.msgprint(str(e[3]))
				frappe.msgprint("Hello")
				if total_hrs >= 2 and e[3]<=3:
					rm=int(e[3])
					rm = rm +1
					incr =int(rm)
					frappe.msgprint(str(incr))
				elif total_hrs >= 2 and e[3]>3:
					incr = e[3]
				frappe.db.set_value("Sales Order", e[0], "cfo_mail_sent", incr)
				frappe.msgprint("Updated")
				if total_hrs >= 2 and e[3]<=3:
					html = """<html><head></head><body><p>"""+ e[0] + """ is pending for Approval</p></body></html>"""
					if bdm == "kartik@tablix.ae" or bdm == "gopu@tablix.ae":
						sales_rep = "remriz.estella@tablix.ae"
					frappe.sendmail(recipients = sales_rep,
						subject=_("{0} is pending for Approvel").format(e[0]),
						message=_("""{0}""").format(html),
						reply_to= sales_rep)
				elif total_hrs >= 2 and e[3] > 3:
					html = """<html><head></head><body><p>"""+ e[0] + """ is not approved by """ +final+ """ </p></body></html>"""
					frappe.sendmail(recipients = "gopu@tablix.ae",
						subject=_("{0} is pending for Approvel").format(e[0]),
						message=_("""{0}""").format(html),
						reply_to= "gopu@tablix.ae")
				else:
					frappe.msgprint("Email is not sent heigher person")	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

@frappe.whitelist()
def close_or_unclose_sales_orders(names, status):
	if not frappe.has_permission("Sales Order", "write"):
		frappe.throw(_("Not permitted"), frappe.PermissionError)

	names = json.loads(names)
	for name in names:
		so = frappe.get_doc("Sales Order", name)
		if so.docstatus == 1:
			if status == "Closed":
				if so.status not in ("Cancelled", "Closed") and (so.per_delivered < 100 or so.per_billed < 100):
					so.update_status(status)
			else:
				if so.status == "Closed":
					so.update_status('Draft')

	frappe.local.message_log = []

@frappe.whitelist()
def make_material_request(source_name, target_doc=None):
	def postprocess(source, doc):
		doc.material_request_type = "Purchase"

	def update_item(source, target, source_parent):
		target.project = source_parent.project

	doc = get_mapped_doc("Sales Order", source_name, {
		"Sales Order": {
			"doctype": "Material Request",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Packed Item": {
			"doctype": "Material Request Item",
			"field_map": {
				"parent": "sales_order",
				"stock_uom": "uom"
			},
			"postprocess": update_item
		},
		"Sales Order Item": {
			"doctype": "Material Request Item",
			"field_map": {
				"parent": "sales_order",
<<<<<<< HEAD
				"stock_uom": "uom",
				"stock_qty": "qty"
=======
				"stock_uom": "uom"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			},
			"condition": lambda doc: not frappe.db.exists('Product Bundle', doc.item_code),
			"postprocess": update_item
		}
	}, target_doc, postprocess)

	return doc

@frappe.whitelist()
<<<<<<< HEAD
def make_project(source_name, target_doc=None):
	def postprocess(source, doc):
		doc.project_type = "External"
		doc.project_name = source.name

	doc = get_mapped_doc("Sales Order", source_name, {
		"Sales Order": {
			"doctype": "Project",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map":{
				"name" : "sales_order",
				"base_grand_total" : "estimated_costing",
			}
		},
		"Sales Order Item": {
			"doctype": "Project Task",
			"field_map": {
				"description": "title",
			},
		}
	}, target_doc, postprocess)

	return doc

@frappe.whitelist()
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
def make_delivery_note(source_name, target_doc=None):
	def set_missing_values(source, target):
		if source.po_no:
			if target.po_no:
				target_po_no = target.po_no.split(", ")
				target_po_no.append(source.po_no)
				target.po_no = ", ".join(list(set(target_po_no))) if len(target_po_no) > 1 else target_po_no[0]
			else:
				target.po_no = source.po_no

		target.ignore_pricing_rule = 1
		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")
<<<<<<< HEAD
		
		# set company address
		target.update(get_company_address(target.company))
		if target.company_address:
			target.update(get_fetch_values("Delivery Note", 'company_address', target.company_address))
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	def update_item(source, target, source_parent):
		target.base_amount = (flt(source.qty) - flt(source.delivered_qty)) * flt(source.base_rate)
		target.amount = (flt(source.qty) - flt(source.delivered_qty)) * flt(source.rate)
		target.qty = flt(source.qty) - flt(source.delivered_qty)

<<<<<<< HEAD
		item = frappe.db.get_value("Item", target.item_code, ["item_group", "selling_cost_center"], as_dict=1)
		target.cost_center = frappe.db.get_value("Project", source_parent.project, "cost_center") \
			or item.selling_cost_center \
			or frappe.db.get_value("Item Group", item.item_group, "default_cost_center")

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	target_doc = get_mapped_doc("Sales Order", source_name, {
		"Sales Order": {
			"doctype": "Delivery Note",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Sales Order Item": {
			"doctype": "Delivery Note Item",
			"field_map": {
				"rate": "rate",
				"name": "so_detail",
				"parent": "against_sales_order",
			},
			"postprocess": update_item,
			"condition": lambda doc: abs(doc.delivered_qty) < abs(doc.qty) and doc.delivered_by_supplier!=1
		},
		"Sales Taxes and Charges": {
			"doctype": "Sales Taxes and Charges",
			"add_if_empty": True
		},
		"Sales Team": {
			"doctype": "Sales Team",
			"add_if_empty": True
		}
	}, target_doc, set_missing_values)

	return target_doc

@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None, ignore_permissions=False):
	def postprocess(source, target):
		set_missing_values(source, target)
		#Get the advance paid Journal Entries in Sales Invoice Advance
		target.set_advances()

	def set_missing_values(source, target):
		target.is_pos = 0
		target.ignore_pricing_rule = 1
		target.flags.ignore_permissions = True
		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")

<<<<<<< HEAD
		# set company address
		target.update(get_company_address(target.company))
		if target.company_address:
			target.update(get_fetch_values("Sales Invoice", 'company_address', target.company_address))

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def update_item(source, target, source_parent):
		target.amount = flt(source.amount) - flt(source.billed_amt)
		target.base_amount = target.amount * flt(source_parent.conversion_rate)
		target.qty = target.amount / flt(source.rate) if (source.rate and source.billed_amt) else source.qty

<<<<<<< HEAD
		item = frappe.db.get_value("Item", target.item_code, ["item_group", "selling_cost_center"], as_dict=1)
		target.cost_center = frappe.db.get_value("Project", source_parent.project, "cost_center") \
			or item.selling_cost_center \
			or frappe.db.get_value("Item Group", item.item_group, "default_cost_center")

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	doclist = get_mapped_doc("Sales Order", source_name, {
		"Sales Order": {
			"doctype": "Sales Invoice",
			"field_map": {
				"party_account_currency": "party_account_currency"
			},
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Sales Order Item": {
			"doctype": "Sales Invoice Item",
			"field_map": {
				"name": "so_detail",
				"parent": "sales_order",
			},
			"postprocess": update_item,
			"condition": lambda doc: doc.qty and (doc.base_amount==0 or abs(doc.billed_amt) < abs(doc.amount))
		},
		"Sales Taxes and Charges": {
			"doctype": "Sales Taxes and Charges",
			"add_if_empty": True
		},
		"Sales Team": {
			"doctype": "Sales Team",
			"add_if_empty": True
		}
	}, target_doc, postprocess, ignore_permissions=ignore_permissions)

	return doclist

@frappe.whitelist()
def make_maintenance_schedule(source_name, target_doc=None):
	maint_schedule = frappe.db.sql("""select t1.name
		from `tabMaintenance Schedule` t1, `tabMaintenance Schedule Item` t2
		where t2.parent=t1.name and t2.sales_order=%s and t1.docstatus=1""", source_name)

	if not maint_schedule:
		doclist = get_mapped_doc("Sales Order", source_name, {
			"Sales Order": {
				"doctype": "Maintenance Schedule",
				"validation": {
					"docstatus": ["=", 1]
				}
			},
			"Sales Order Item": {
				"doctype": "Maintenance Schedule Item",
				"field_map": {
					"parent": "sales_order"
				},
				"add_if_empty": True
			}
		}, target_doc)

		return doclist

@frappe.whitelist()
def make_maintenance_visit(source_name, target_doc=None):
	visit = frappe.db.sql("""select t1.name
		from `tabMaintenance Visit` t1, `tabMaintenance Visit Purpose` t2
		where t2.parent=t1.name and t2.prevdoc_docname=%s
		and t1.docstatus=1 and t1.completion_status='Fully Completed'""", source_name)

	if not visit:
		doclist = get_mapped_doc("Sales Order", source_name, {
			"Sales Order": {
				"doctype": "Maintenance Visit",
				"validation": {
					"docstatus": ["=", 1]
				}
			},
			"Sales Order Item": {
				"doctype": "Maintenance Visit Purpose",
				"field_map": {
					"parent": "prevdoc_docname",
					"parenttype": "prevdoc_doctype"
				},
				"add_if_empty": True
			}
		}, target_doc)

		return doclist

@frappe.whitelist()
def get_events(start, end, filters=None):
	"""Returns events for Gantt / Calendar view rendering.

	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	from frappe.desk.calendar import get_event_conditions
	conditions = get_event_conditions("Sales Order", filters)

<<<<<<< HEAD
	data = frappe.db.sql("""
		select
			`tabSales Order`.name, `tabSales Order`.customer_name, `tabSales Order`.status,
			`tabSales Order`.delivery_status, `tabSales Order`.billing_status,
			`tabSales Order Item`.delivery_date
		from
			`tabSales Order`, `tabSales Order Item`
		where `tabSales Order`.name = `tabSales Order Item`.parent
			and (ifnull(`tabSales Order Item`.delivery_date, '0000-00-00')!= '0000-00-00') \
			and (`tabSales Order Item`.delivery_date between %(start)s and %(end)s)
			and `tabSales Order`.docstatus < 2
			{conditions}
=======
	data = frappe.db.sql("""select name, customer_name, delivery_status, billing_status, delivery_date
		from `tabSales Order`
		where (ifnull(delivery_date, '0000-00-00')!= '0000-00-00') \
				and (delivery_date between %(start)s and %(end)s)
				and docstatus < 2
				{conditions}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		""".format(conditions=conditions), {
			"start": start,
			"end": end
		}, as_dict=True, update={"allDay": 0})
	return data

@frappe.whitelist()
def make_purchase_order_for_drop_shipment(source_name, for_supplier, target_doc=None):
	def set_missing_values(source, target):
		target.supplier = for_supplier
		target.apply_discount_on = ""
		target.additional_discount_percentage = 0.0
		target.discount_amount = 0.0

		default_price_list = frappe.get_value("Supplier", for_supplier, "default_price_list")
		if default_price_list:
			target.buying_price_list = default_price_list

		if any( item.delivered_by_supplier==1 for item in source.items):
			if source.shipping_address_name:
				target.shipping_address = source.shipping_address_name
				target.shipping_address_display = source.shipping_address
			else:
				target.shipping_address = source.customer_address
				target.shipping_address_display = source.address_display

			target.customer_contact_person = source.contact_person
			target.customer_contact_display = source.contact_display
			target.customer_contact_mobile = source.contact_mobile
			target.customer_contact_email = source.contact_email

		else:
			target.customer = ""
			target.customer_name = ""

		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")

	def update_item(source, target, source_parent):
<<<<<<< HEAD
		target.schedule_date = source.delivery_date
		target.qty = flt(source.qty) - flt(source.ordered_qty)
		target.stock_qty = (flt(source.qty) - flt(source.ordered_qty)) * flt(source.conversion_factor)
=======
		target.schedule_date = source_parent.delivery_date
		target.qty = flt(source.qty) - flt(source.ordered_qty)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	doclist = get_mapped_doc("Sales Order", source_name, {
		"Sales Order": {
			"doctype": "Purchase Order",
			"field_no_map": [
				"address_display",
				"contact_display",
				"contact_mobile",
				"contact_email",
				"contact_person"
			],
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Sales Order Item": {
			"doctype": "Purchase Order Item",
			"field_map":  [
				["name", "sales_order_item"],
				["parent", "sales_order"],
<<<<<<< HEAD
				["stock_uom", "stock_uom"],
				["uom", "uom"],
				["conversion_factor", "conversion_factor"],
=======
				["uom", "stock_uom"],
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				["delivery_date", "schedule_date"]
			],
			"field_no_map": [
				"rate",
				"price_list_rate"
			],
			"postprocess": update_item,
			"condition": lambda doc: doc.ordered_qty < doc.qty and doc.supplier == for_supplier
		}
	}, target_doc, set_missing_values)

	return doclist

@frappe.whitelist()
def get_supplier(doctype, txt, searchfield, start, page_len, filters):
	supp_master_name = frappe.defaults.get_user_default("supp_master_name")
	if supp_master_name == "Supplier Name":
		fields = ["name", "supplier_type"]
	else:
		fields = ["name", "supplier_name", "supplier_type"]
	fields = ", ".join(fields)

	return frappe.db.sql("""select {field} from `tabSupplier`
		where docstatus < 2
			and ({key} like %(txt)s
				or supplier_name like %(txt)s)
			and name in (select supplier from `tabSales Order Item` where parent = %(parent)s)
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, supplier_name), locate(%(_txt)s, supplier_name), 99999),
			name, supplier_name
		limit %(start)s, %(page_len)s """.format(**{
			'field': fields,
			'key': frappe.db.escape(searchfield)
		}), {
			'txt': "%%%s%%" % txt,
			'_txt': txt.replace("%", ""),
			'start': start,
			'page_len': page_len,
			'parent': filters.get('parent')
		})
<<<<<<< HEAD

@frappe.whitelist()
def make_production_orders(items, sales_order, company, project=None):
	'''Make Production Orders against the given Sales Order for the given `items`'''
	items = json.loads(items).get('items')
	out = []

	for i in items:
		production_order = frappe.get_doc(dict(
			doctype='Production Order',
			production_item=i['item_code'],
			bom_no=i['bom'],
			qty=i['pending_qty'],
			company=company,
			sales_order=sales_order,
			project=project,
			fg_warehouse=i['warehouse']
		)).insert()
		production_order.set_production_order_operations()
		production_order.save()
		out.append(production_order)

	return [p.name for p in out]
=======
		
@frappe.whitelist()
def make_preventive_maintenance(source_name, target_doc=None):
	doclist = get_mapped_doc("Sales Order", source_name, {
	"Sales Order": {
			"doctype": "Maintenance Contract",
			"field_map": {
				"name": "so_number",
				"amc_type": "amc_type",
				"amc_duration": "amc_duration",
				"project_site_name": "site_name",
				"customer": "customer",
				"po_no": "po_no",
				"po_date": "po_date"
			}
		},
		
		"Sales Order Item": {
			"doctype": "Preventive Maintenance Item",
			"field_map": {
				"item_code": "item_code",
				"amc_type": "amc_type",
				"item_name": "item_name",
				"qty": "qty",
				"brand": "brand",
				"description": "description"
			}
		}
	},target_doc)
		
	return doclist		

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

@frappe.whitelist()
def update_status(status, name):
	so = frappe.get_doc("Sales Order", name)
	so.update_status(status)
<<<<<<< HEAD

def get_default_bom_item(item_code):
	bom = frappe.get_all('BOM', dict(item=item_code, is_active=True),
			order_by='is_default desc')
	bom = bom[0].name if bom else None

	return bom
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
