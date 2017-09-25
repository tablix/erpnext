# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# ERPNext - web based ERP (http://erpnext.com)
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

<<<<<<< HEAD
from frappe.utils import cstr, flt, getdate, new_line_sep
=======
from frappe.utils import cstr, flt, getdate, new_line_sep, get_link_to_form, money_in_words
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
from frappe import msgprint, _
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.stock_balance import update_bin_qty, get_indented_qty
from erpnext.controllers.buying_controller import BuyingController
from erpnext.manufacturing.doctype.production_order.production_order import get_item_details
<<<<<<< HEAD
from erpnext.buying.utils import check_for_closed_status, validate_for_items
=======
from frappe.desk.form import assign_to

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

form_grid_templates = {
	"items": "templates/form_grid/material_request_grid.html"
}

class MaterialRequest(BuyingController):
	def get_feed(self):
		return _("{0}: {1}").format(self.status, self.material_request_type)

	def check_if_already_pulled(self):
		pass

	def validate_qty_against_so(self):
		so_items = {} # Format --> {'SO/00001': {'Item/001': 120, 'Item/002': 24}}
		for d in self.get('items'):
			if d.sales_order:
				if not so_items.has_key(d.sales_order):
					so_items[d.sales_order] = {d.item_code: flt(d.qty)}
				else:
					if not so_items[d.sales_order].has_key(d.item_code):
						so_items[d.sales_order][d.item_code] = flt(d.qty)
					else:
						so_items[d.sales_order][d.item_code] += flt(d.qty)

		for so_no in so_items.keys():
			for item in so_items[so_no].keys():
				already_indented = frappe.db.sql("""select sum(qty)
					from `tabMaterial Request Item`
					where item_code = %s and sales_order = %s and
					docstatus = 1 and parent != %s""", (item, so_no, self.name))
				already_indented = already_indented and flt(already_indented[0][0]) or 0

<<<<<<< HEAD
				actual_so_qty = frappe.db.sql("""select sum(stock_qty) from `tabSales Order Item`
=======
				actual_so_qty = frappe.db.sql("""select sum(qty) from `tabSales Order Item`
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
					where parent = %s and item_code = %s and docstatus = 1""", (so_no, item))
				actual_so_qty = actual_so_qty and flt(actual_so_qty[0][0]) or 0

				if actual_so_qty and (flt(so_items[so_no][item]) + already_indented > actual_so_qty):
					frappe.throw(_("Material Request of maximum {0} can be made for Item {1} against Sales Order {2}").format(actual_so_qty - already_indented, item, so_no))

	def validate_schedule_date(self):
		for d in self.get('items'):
			if d.schedule_date and getdate(d.schedule_date) < getdate(self.transaction_date):
				frappe.throw(_("Expected Date cannot be before Material Request Date"))

	# Validate
	# ---------------------
	def validate(self):
		super(MaterialRequest, self).validate()

		self.validate_schedule_date()
		self.validate_uom_is_integer("uom", "qty")

		if not self.status:
			self.status = "Draft"
<<<<<<< HEAD

		from erpnext.controllers.status_updater import validate_status
		validate_status(self.status, ["Draft", "Submitted", "Stopped", "Cancelled", "Pending",
										"Partially Ordered", "Ordered", "Issued", "Transferred"]
						)

		validate_for_items(self)

		# self.set_title()
		# self.validate_qty_against_so()
		# NOTE: Since Item BOM and FG quantities are combined, using current data, it cannot be validated
		# Though the creation of Material Request from a Production Plan can be rethought to fix this
=======
		
		proj = self.project	
		frappe.db.set(self, 'project_name', proj)
		frappe.db.commit()
		
		from erpnext.controllers.status_updater import validate_status
		validate_status(self.status, ["Draft", "Submitted", "Stopped", "Cancelled"])

		pc_obj = frappe.get_doc('Purchase Common')
		pc_obj.validate_for_items(self)
		
		
		#new addition
		#self.validate_item_code()
		# self.set_title()


		# self.validate_qty_against_so()
		# NOTE: Since Item BOM and FG quantities are combined, using current data, it cannot be validated
		# Though the creation of Material Request from a Production Plan can be rethought to fix this
		
	
	#new addition
	
	def validate_item_code(self):
		 so = self.customer_order
		 if so is not None and so != "":
			 for d in self.get("items"):
				 item_code = frappe.db.get_value("Sales Order Item", {"parent":so, "item_code":d.item_code})
				 if item_code is None:
					frappe.throw(_("Item {0}: Item is not available in SO.").format(d.item_code))
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	def set_title(self):
		'''Set title as comma separated list of items'''
		items = []
		for d in self.items:
			if d.item_code not in items:
				items.append(d.item_code)
			if(len(items)==4):
				break

		self.title = ', '.join(items)

	def on_submit(self):
<<<<<<< HEAD
		# frappe.db.set(self, 'status', 'Submitted')
		self.update_requested_qty()

	def before_save(self):
		self.set_status(update=True)

	def before_submit(self):
		self.set_status(update=True)

	def before_cancel(self):
		# if MRQ is already closed, no point saving the document
		check_for_closed_status(self.doctype, self.name)
		self.set_status(update=True, status='Cancelled')

=======
		if self.approval != "Approved":
			frappe.throw(_("{0} cannot be submitted unless it is in Approved state").format(self.name))
		frappe.db.set(self, 'status', 'Submitted')
		self.update_requested_qty()

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def check_modified_date(self):
		mod_db = frappe.db.sql("""select modified from `tabMaterial Request` where name = %s""",
			self.name)
		date_diff = frappe.db.sql("""select TIMEDIFF('%s', '%s')"""
			% (mod_db[0][0], cstr(self.modified)))

		if date_diff and date_diff[0][0]:
			frappe.throw(_("{0} {1} has been modified. Please refresh.").format(_(self.doctype), self.name))

	def update_status(self, status):
		self.check_modified_date()
<<<<<<< HEAD
		self.status_can_change(status)
		self.set_status(update=True, status=status)
		self.update_requested_qty()

	def status_can_change(self, status):
		"""
		validates that `status` is acceptable for the present controller status
		and throws an Exception if otherwise.
		"""
		if self.status and self.status == 'Cancelled':
			# cancelled documents cannot change
			if status != self.status:
				frappe.throw(
					_("{0} {1} is cancelled so the action cannot be completed").
						format(_(self.doctype), self.name),
					frappe.InvalidStatusError
				)

		elif self.status and self.status == 'Draft':
			# draft document to pending only
			if status != 'Pending':
				frappe.throw(
					_("{0} {1} has not been submitted so the action cannot be completed").
						format(_(self.doctype), self.name),
					frappe.InvalidStatusError
				)

	def on_cancel(self):
		self.update_requested_qty()

=======
		frappe.db.set(self, 'status', cstr(status))
		self.update_requested_qty()

	def on_cancel(self):
		pc_obj = frappe.get_doc('Purchase Common')

		pc_obj.check_for_closed_status(self.doctype, self.name)

		self.update_requested_qty()

		frappe.db.set(self,'status','Cancelled')

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def update_completed_qty(self, mr_items=None, update_modified=True):
		if self.material_request_type == "Purchase":
			return

		if not mr_items:
			mr_items = [d.name for d in self.get("items")]

		for d in self.get("items"):
			if d.name in mr_items:
				if self.material_request_type in ("Material Issue", "Material Transfer"):
					d.ordered_qty =  flt(frappe.db.sql("""select sum(transfer_qty)
						from `tabStock Entry Detail` where material_request = %s
						and material_request_item = %s and docstatus = 1""",
						(self.name, d.name))[0][0])

					if d.ordered_qty and d.ordered_qty > d.qty:
						frappe.throw(_("The total Issue / Transfer quantity {0} in Material Request {1}  \
							cannot be greater than requested quantity {2} for Item {3}").format(d.ordered_qty, d.parent, d.qty, d.item_code))

				elif self.material_request_type == "Manufacture":
					d.ordered_qty = flt(frappe.db.sql("""select sum(qty)
						from `tabProduction Order` where material_request = %s
						and material_request_item = %s and docstatus = 1""",
						(self.name, d.name))[0][0])

				frappe.db.set_value(d.doctype, d.name, "ordered_qty", d.ordered_qty)

		self._update_percent_field({
			"target_dt": "Material Request Item",
			"target_parent_dt": self.doctype,
			"target_parent_field": "per_ordered",
			"target_ref_field": "qty",
			"target_field": "ordered_qty",
			"name": self.name,
		}, update_modified)

	def update_requested_qty(self, mr_item_rows=None):
		"""update requested qty (before ordered_qty is updated)"""
		item_wh_list = []
		for d in self.get("items"):
			if (not mr_item_rows or d.name in mr_item_rows) and [d.item_code, d.warehouse] not in item_wh_list \
					and frappe.db.get_value("Item", d.item_code, "is_stock_item") == 1 and d.warehouse:
				item_wh_list.append([d.item_code, d.warehouse])

		for item_code, warehouse in item_wh_list:
			update_bin_qty(item_code, warehouse, {
				"indented_qty": get_indented_qty(item_code, warehouse)
			})
<<<<<<< HEAD
=======
	
	#new addition
	def send_notification(self, reason, remark=""):
		commercial_mgnr = "heena@tablix.ae"
		if self.project_name is None:
			project_name = self.project
		else:
			project_name = self.project_name
			
		if project_name is None:
			project_name = ""
		owner = self.owner
		
		#msgprint("Entry")
		if reason == "cm_review":
			val = 0
			if (self.approval == "Open" or self.approval == "Commercial Rejected"):
				#msgprint("Approval")
				self.notify_employee(commercial_mgnr, project_name, val)
				frappe.db.set_value("Material Request", self.name, "approval", "Commercial Review")
			else:
				self.notify_employee(commercial_mgnr, project_name, val)
				frappe.db.set_value("Material Request", self.name, "assigned", 1)
			frappe.db.set_value("Material Request", self.name, "reason", "")
			frappe.db.commit()
				
		elif reason == "cm_approved":
			val = 1
			so_no = 420
			so = 0
			if self.customer_order is not None and self.customer_order != "":
				#msgprint("Success!!")
				so = self.customer_order
				so = so.replace("SO-", "")
				so = so.split("-")
				so = int(so[0])
			if self.customer_order is not None :
				if so > so_no:
					self.notify_employee(owner, project_name, val)
			frappe.db.set_value("Material Request", self.name, "approval", "Approved")
			frappe.db.set_value("Material Request", self.name, "reason", "")
			frappe.db.commit()
		
		elif reason == "cm_rejected":
			val = 2
			self.notify_employee(owner, project_name, val)
			frappe.db.set_value("Material Request", self.name, "approval", "Commercial Rejected")
			frappe.db.set_value("Material Request", self.name, "reason", remark)
			frappe.db.commit()
			
		elif reason == "kam_review":
			val = 0
			acc_manager = frappe.db.get_value("Sales Order", self.customer_order, "account_manager")
			self.notify_employee(acc_manager, project_name, val)
			frappe.db.set_value("Material Request", self.name, "approval", "KAM Review")
			frappe.db.commit()
		
		elif reason == "kam_approved":
			val = 3
			self.notify_employee(owner, project_name, val)
			frappe.db.set_value("Material Request", self.name, "approval", "Approved")
			frappe.db.set_value("Material Request", self.name, "reason", "")
			frappe.db.commit()
			
		elif reason == "kam_rejected":
			val = 4
			self.notify_employee(owner, project_name, val)
			frappe.db.set_value("Material Request", self.name, "approval", "KAM Rejected")
			frappe.db.set_value("Material Request", self.name, "reason", remark)
			frappe.db.commit()
			
		return True
	
	
	def notify_employee(self, employee, subject, val):
		
		
		#msgprint("Success" + str(val))
		
		def _get_message(url=False):
			if url:
				name = get_link_to_form(self.doctype, self.name)
			else:
				name = self.name
			if val == 0:
				return (_("MR")+ "- %s" + _("assigned for approval") + ": %s") % (subject, name)
			elif val ==1:
				return (_("MR")+ "- %s " + _("approved by Commercial Manager") + ": %s") % (subject, name)
			elif val == 2:
				return (_("MR")+ "- %s " + _("rejected by Commercial Manager") + ": %s") % (subject, name)
			elif val == 3:
				return (_("MR")+ "- %s " + _("approved by KAM") + ": %s") % (subject, name)
			elif val == 4:
				return (_("MR")+ "- %s " + _("rejected by KAM") + ": %s") % (subject, name)
			
		
			
		self.notify({
			# for post in messages
			"message": _get_message(url=True),
			"message_to": employee,
			"subject": _get_message(),
			"subject": _get_message(),
		})
	
		desc = ''	
		assign_to.clear(self.doctype, self.name)
		proj_name = subject.encode('ascii','ignore')
		if val == 0:
			desc = "MR- " + str(proj_name) + " requies approval"
		elif (val == 1 or val == 3):
			desc = "MR- " + str(proj_name) + " approved"
		elif val == 2:
			desc = "MR- " + str(proj_name) + " rejected by Commercial Manager"
		elif val == 4:
			desc = "MR- " + str(proj_name) + " rejected by KAM"
			
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
		
		
		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

def update_completed_and_requested_qty(stock_entry, method):
	if stock_entry.doctype == "Stock Entry":
		material_request_map = {}

		for d in stock_entry.get("items"):
			if d.material_request:
				material_request_map.setdefault(d.material_request, []).append(d.material_request_item)

		for mr, mr_item_rows in material_request_map.items():
			if mr and mr_item_rows:
				mr_obj = frappe.get_doc("Material Request", mr)

				if mr_obj.status in ["Stopped", "Cancelled"]:
					frappe.throw(_("{0} {1} is cancelled or stopped").format(_("Material Request"), mr),
						frappe.InvalidStatusError)

				mr_obj.update_completed_qty(mr_item_rows)
				mr_obj.update_requested_qty(mr_item_rows)

def set_missing_values(source, target_doc):
	target_doc.run_method("set_missing_values")
	target_doc.run_method("calculate_taxes_and_totals")

def update_item(obj, target, source_parent):
	target.conversion_factor = 1
	target.qty = flt(obj.qty) - flt(obj.ordered_qty)
	target.stock_qty = target.qty

@frappe.whitelist()
def make_purchase_order(source_name, target_doc=None):
	def postprocess(source, target_doc):
		set_missing_values(source, target_doc)

	doclist = get_mapped_doc("Material Request", source_name, 	{
		"Material Request": {
			"doctype": "Purchase Order",
			"validation": {
				"docstatus": ["=", 1],
				"material_request_type": ["=", "Purchase"]
			}
		},
		"Material Request Item": {
			"doctype": "Purchase Order Item",
			"field_map": [
				["name", "material_request_item"],
				["parent", "material_request"],
				["uom", "stock_uom"],
				["uom", "uom"]
			],
			"postprocess": update_item,
			"condition": lambda doc: doc.ordered_qty < doc.qty
		}
	}, target_doc, postprocess)

	return doclist

@frappe.whitelist()
def make_request_for_quotation(source_name, target_doc=None):
	doclist = get_mapped_doc("Material Request", source_name, 	{
		"Material Request": {
			"doctype": "Request for Quotation",
			"validation": {
				"docstatus": ["=", 1],
				"material_request_type": ["=", "Purchase"]
			}
		},
		"Material Request Item": {
			"doctype": "Request for Quotation Item",
			"field_map": [
				["name", "material_request_item"],
				["parent", "material_request"],
				["uom", "uom"]
			]
		}
	}, target_doc)

	return doclist

@frappe.whitelist()
def make_purchase_order_based_on_supplier(source_name, target_doc=None):
	if target_doc:
		if isinstance(target_doc, basestring):
			import json
			target_doc = frappe.get_doc(json.loads(target_doc))
		target_doc.set("items", [])

	material_requests, supplier_items = get_material_requests_based_on_supplier(source_name)

	def postprocess(source, target_doc):
		target_doc.supplier = source_name

		target_doc.set("items", [d for d in target_doc.get("items")
			if d.get("item_code") in supplier_items and d.get("qty") > 0])

		set_missing_values(source, target_doc)

	for mr in material_requests:
		target_doc = get_mapped_doc("Material Request", mr, 	{
			"Material Request": {
				"doctype": "Purchase Order",
			},
			"Material Request Item": {
				"doctype": "Purchase Order Item",
				"field_map": [
					["name", "material_request_item"],
					["parent", "material_request"],
					["uom", "stock_uom"],
					["uom", "uom"]
				],
				"postprocess": update_item,
				"condition": lambda doc: doc.ordered_qty < doc.qty
			}
		}, target_doc, postprocess)

	return target_doc

def get_material_requests_based_on_supplier(supplier):
	supplier_items = [d[0] for d in frappe.db.get_values("Item",
		{"default_supplier": supplier})]
	if supplier_items:
		material_requests = frappe.db.sql_list("""select distinct mr.name
			from `tabMaterial Request` mr, `tabMaterial Request Item` mr_item
			where mr.name = mr_item.parent
			and mr_item.item_code in (%s)
			and mr.material_request_type = 'Purchase'
			and mr.per_ordered < 99.99
			and mr.docstatus = 1
			and mr.status != 'Stopped'
                        order by mr_item.item_code ASC""" % ', '.join(['%s']*len(supplier_items)),
			tuple(supplier_items))
	else:
		material_requests = []
	return material_requests, supplier_items

@frappe.whitelist()
def make_supplier_quotation(source_name, target_doc=None):
	def postprocess(source, target_doc):
		set_missing_values(source, target_doc)

	doclist = get_mapped_doc("Material Request", source_name, {
		"Material Request": {
			"doctype": "Supplier Quotation",
			"validation": {
				"docstatus": ["=", 1],
				"material_request_type": ["=", "Purchase"]
			}
		},
		"Material Request Item": {
			"doctype": "Supplier Quotation Item",
			"field_map": {
				"name": "material_request_item",
				"parent": "material_request"
			}
		}
	}, target_doc, postprocess)

	return doclist

@frappe.whitelist()
def make_stock_entry(source_name, target_doc=None):
	def update_item(obj, target, source_parent):
		qty = flt(obj.qty) - flt(obj.ordered_qty) \
			if flt(obj.qty) > flt(obj.ordered_qty) else 0
		target.qty = qty
		target.transfer_qty = qty
		target.conversion_factor = 1

		if source_parent.material_request_type == "Material Transfer":
			target.t_warehouse = obj.warehouse
		else:
			target.s_warehouse = obj.warehouse

	def set_missing_values(source, target):
		target.purpose = source.material_request_type
		target.run_method("calculate_rate_and_amount")

	doclist = get_mapped_doc("Material Request", source_name, {
		"Material Request": {
			"doctype": "Stock Entry",
			"validation": {
				"docstatus": ["=", 1],
				"material_request_type": ["in", ["Material Transfer", "Material Issue"]]
			}
		},
		"Material Request Item": {
			"doctype": "Stock Entry Detail",
			"field_map": {
				"name": "material_request_item",
				"parent": "material_request",
				"uom": "stock_uom",
			},
			"postprocess": update_item,
			"condition": lambda doc: doc.ordered_qty < doc.qty
		}
	}, target_doc, set_missing_values)

	return doclist

@frappe.whitelist()
def raise_production_orders(material_request):
	mr= frappe.get_doc("Material Request", material_request)
	errors =[]
	production_orders = []
<<<<<<< HEAD
	default_wip_warehouse = frappe.db.get_single_value("Manufacturing Settings", "default_wip_warehouse")
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	for d in mr.items:
		if (d.qty - d.ordered_qty) >0:
			if frappe.db.get_value("BOM", {"item": d.item_code, "is_default": 1}):
				prod_order = frappe.new_doc("Production Order")
				prod_order.production_item = d.item_code
				prod_order.qty = d.qty - d.ordered_qty
				prod_order.fg_warehouse = d.warehouse
<<<<<<< HEAD
				prod_order.wip_warehouse = default_wip_warehouse
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				prod_order.description = d.description
				prod_order.stock_uom = d.uom
				prod_order.expected_delivery_date = d.schedule_date
				prod_order.sales_order = d.sales_order
				prod_order.bom_no = get_item_details(d.item_code).bom_no
				prod_order.material_request = mr.name
				prod_order.material_request_item = d.name
				prod_order.planned_start_date = mr.transaction_date
				prod_order.company = mr.company
				prod_order.save()
				production_orders.append(prod_order.name)
			else:
<<<<<<< HEAD
				errors.append(_("Row {0}: Bill of Materials not found for the Item {1}").format(d.idx, d.item_code))
	if production_orders:
		message = ["""<a href="#Form/Production Order/%s" target="_blank">%s</a>""" % \
			(p, p) for p in production_orders]
		msgprint(_("The following Production Orders were created:") + '\n' + new_line_sep(message))
	if errors:
		frappe.throw(_("Productions Orders cannot be raised for:") + '\n' + new_line_sep(errors))
=======
				errors.append(d.item_code + " in Row " + cstr(d.idx))
	if production_orders:
		message = ["""<a href="#Form/Production Order/%s" target="_blank">%s</a>""" % \
			(p, p) for p in production_orders]
		msgprint(_("The following Production Orders were created:" + '\n' + new_line_sep(message)))
	if errors:
		msgprint(_("Productions Orders cannot be raised for:" + '\n' + new_line_sep(errors)))
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	return production_orders
