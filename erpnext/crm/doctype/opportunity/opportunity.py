# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.utils import cstr, cint, get_fullname, get_link_to_form
from frappe import msgprint, _
from frappe.model.mapper import get_mapped_doc
from erpnext.setup.utils import get_exchange_rate
from erpnext.utilities.transaction_base import TransactionBase
from erpnext.accounts.party import get_party_account_currency
from frappe.desk.form import assign_to
import datetime


subject_field = "title"
sender_field = "contact_email"
cbdo = "kartik@tablix.ae"
coo = "satyajith.ashokan@tablix.ae"
cto = "ali@tablix.ae"
ceo = "gopu@tablix.ae"
security_engg1 = "lathesh@tablix.ae"
security_engg2 = "dafni.prabhakaran@tablix.ae"
security_engg3 = "prashanth@tablix.ae"
av_engg = "arjun.e@tablix.ae"
bms_engg = "aleem.abrar@tablix.ae"
ba_engg = "anil@tablix.ae"
sales_coordinator = "remriz.estella@tablix.ae"

class Opportunity(TransactionBase):
	def after_insert(self):
		if self.lead:
			frappe.get_doc("Lead", self.lead).set_status(update=True)

	def validate(self):
		#new addittion
		for d in self.s:
			if d.type in ('CCTV, ANPR, ICT, ACS, VSB, Fit out, Parking Management, PCS'):
				self.type = "Security systems"
			else:
				self.type = d.type
			self.solution = d.type
		if self.tender == "Yes":
			self.is_proposal = 1
			
		if self.is_amc == 0 and self.boq == 0:
			msgprint("Kindly select either Project or AMC")
			
		self._prev = frappe._dict({
			"contact_date": frappe.db.get_value("Opportunity", self.name, "contact_date") if 
				(not cint(self.get("__islocal"))) else None,
			"contact_by": frappe.db.get_value("Opportunity", self.name, "contact_by") if \
				(not cint(self.get("__islocal"))) else None,
		})

		self.make_new_lead_if_required()

		if not self.enquiry_from:
			frappe.throw(_("Opportunity From field is mandatory"))

		self.set_status()
		self.validate_item_details()
		self.validate_uom_is_integer("uom", "qty")
		self.validate_lead_cust()
		self.validate_cust_name()

		if not self.title:
			self.title = self.customer_name


	def make_new_lead_if_required(self):
		"""Set lead against new opportunity"""
		if not (self.lead or self.customer) and self.contact_email:
			lead_name = frappe.db.get_value("Lead", {"email_id": self.contact_email})
			if not lead_name:
				sender_name = get_fullname(self.contact_email)
				if sender_name == self.contact_email:
					sender_name = None

				if not sender_name and ('@' in self.contact_email):
					email_name = self.contact_email.split('@')[0]

					email_split = email_name.split('.')
					sender_name = ''
					for s in email_split:
						sender_name += s.capitalize() + ' '

				lead = frappe.get_doc({
					"doctype": "Lead",
					"email_id": self.contact_email,
					"lead_name": sender_name
				})

				lead.flags.ignore_email_validation = True
				lead.insert(ignore_permissions=True)
				lead_name = lead.name

			self.enquiry_from = "Lead"
			self.lead = lead_name

	def declare_enquiry_lost(self,arg):
		if not self.has_quotation():
			frappe.db.set(self, 'status', 'Lost')
			frappe.db.set(self, 'order_lost_reason', arg)
		else:
			frappe.throw(_("Cannot declare as lost, because Quotation has been made."))

	def on_trash(self):
		self.delete_events()

	def has_quotation(self):
		return frappe.db.get_value("Quotation Item", {"prevdoc_docname": self.name, "docstatus": 1})

	def has_ordered_quotation(self):
		return frappe.db.sql("""select q.name from `tabQuotation` q, `tabQuotation Item` qi
			where q.name = qi.parent and q.docstatus=1 and qi.prevdoc_docname =%s and q.status = 'Ordered'""", self.name)

	def validate_cust_name(self):
		if self.customer:
			self.customer_name = frappe.db.get_value("Customer", self.customer, "customer_name")
		elif self.lead:
			lead_name, company_name = frappe.db.get_value("Lead", self.lead, ["lead_name", "company_name"])
			self.customer_name = company_name or lead_name

	def get_cust_address(self,name):
		details = frappe.db.sql("""select customer_name, address, territory, customer_group
			from `tabCustomer` where name = %s and docstatus != 2""", (name), as_dict = 1)
		if details:
			ret = {
				'customer_name':	details and details[0]['customer_name'] or '',
				'address'	:	details and details[0]['address'] or '',
				'territory'			 :	details and details[0]['territory'] or '',
				'customer_group'		:	details and details[0]['customer_group'] or ''
			}
			# ********** get primary contact details (this is done separately coz. , in case there is no primary contact thn it would not be able to fetch customer details in case of join query)

			contact_det = frappe.db.sql("""select contact_name, contact_no, email_id
				from `tabContact` where customer = %s and is_customer = 1
					and is_primary_contact = 'Yes' and docstatus != 2""", name, as_dict = 1)

			ret['contact_person'] = contact_det and contact_det[0]['contact_name'] or ''
			ret['contact_no']		 = contact_det and contact_det[0]['contact_no'] or ''
			ret['email_id']			 = contact_det and contact_det[0]['email_id'] or ''

			return ret
		else:
			frappe.throw(_("Customer {0} does not exist").format(name), frappe.DoesNotExistError)

	def on_update(self):
		self.add_calendar_event()

	def add_calendar_event(self, opts=None, force=False):
		if not opts:
			opts = frappe._dict()

		opts.description = ""
		opts.contact_date = self.contact_date

		if self.customer:
			if self.contact_person:
				opts.description = 'Contact '+cstr(self.contact_person)
			else:
				opts.description = 'Contact customer '+cstr(self.customer)
		elif self.lead:
			if self.contact_display:
				opts.description = 'Contact '+cstr(self.contact_display)
			else:
				opts.description = 'Contact lead '+cstr(self.lead)

		opts.subject = opts.description
		opts.description += '. By : ' + cstr(self.contact_by)

		if self.to_discuss:
			opts.description += ' To Discuss : ' + cstr(self.to_discuss)

		super(Opportunity, self).add_calendar_event(opts, force)

	def validate_item_details(self):
		if not self.get('items'):
			return

		# set missing values
		item_fields = ("item_name", "description", "item_group", "brand")

		for d in self.items:
			if not d.item_code:
				continue

			item = frappe.db.get_value("Item", d.item_code, item_fields, as_dict=True)
			for key in item_fields:
				if not d.get(key): d.set(key, item.get(key))

	def validate_lead_cust(self):
		if self.enquiry_from == 'Lead':
			if not self.lead:
				frappe.throw(_("Lead must be set if Opportunity is made from Lead"))
			else:
				self.customer = None
		elif self.enquiry_from == 'Customer':
			if not self.customer:
				msgprint("Customer is mandatory if 'Opportunity From' is selected as Customer", raise_exception=1)
			else:
				self.lead = None
				
	#new addition
	def insufficient_info_remark(self):
		#msgprint("+++++")
		remark = frappe.db.get_value("Opportunity", self.name, 'to_discuss')
		#msgprint("Value: " + remark)
		return remark	
		
	def approval(self, approval_person):
		project_name = frappe.db.get_value("Opportunity", self.name, 'project_name')
		opp_creator = frappe.db.get_value("Opportunity", self.name, 'bdm')
		type = frappe.db.get_value("Opportunity", self.name, 'type')
		customer_name = frappe.db.get_value("Opportunity", self.name, 'customer_name')
		
		if approval_person == 'SAM':
			sam = frappe.db.get_value("Opportunity", self.name, 'account_manager')
			if sam == coo:
				val = 0
				frappe.db.set_value("Opportunity", self.name, "status", "COO Approved")
				cur_date=datetime.datetime.now()
				cur_date = cur_date.strftime('%Y-%m-%d %H:%M:%S')
				frappe.db.set_value("Opportunity", self.name, "coo_date_time", cur_date)
				self.notify_employee(cbdo, project_name, val, 1, customer_name)
				val = 4
				self.notify_employee(opp_creator, project_name, val, 0, customer_name)
				if opp_creator == ceo or opp_creator == cbdo or opp_creator == coo:
					self.notify_employee(sales_coordinator, project_name, val, 0, customer_name)
			else:
				val = 0
				frappe.db.set_value("Opportunity", self.name, "status", "KAM Approved")
				cur_date=datetime.datetime.now()
				cur_date = cur_date.strftime('%Y-%m-%d %H:%M:%S')
				frappe.db.set_value("Opportunity", self.name, "kam_date_time", cur_date)
				self.notify_employee(coo, project_name, val, 1, customer_name)
				val = 4
				self.notify_employee(opp_creator, project_name, val, 0, customer_name)
				if opp_creator == ceo or opp_creator == cbdo or opp_creator == coo:
					self.notify_employee(sales_coordinator, project_name, val, 0, customer_name)
					
		elif approval_person == "COO":
			sam = frappe.db.get_value("Opportunity", self.name, 'account_manager')
			if sam == cbdo:
				frappe.db.set_value("Opportunity", self.name, "status", "RFQ Approved")
				if self.enquiry_from == "Lead" and self.lead is not None:
					#cust_email_id = frappe.db.get_value("Lead", self.lead , "email_id")
					cust_email_id = frappe.db.get_value("Opportunity" , self.name , "contact_email")
					#frappe.msgprint(str(cust_email_id))
					e = frappe.db.get_value('Employee',{'user_id' : self.bdm}, ['employee_name', 'designation' , 'user_id' , 'cell_number'])
					#frappe.msgprint(str(e))
					e_name = str(e[0])
					desg = str(e[1])
					u_id = str(e[2])
					no = str(e[3])
					if no.startswith('0'):
						no=no.replace('0','+971 ')
						#frappe.msgprint(no)
					if '+971' not in no and no != None:
						no = '+971 ' + no
						#frappe.msgprint(no)
					if e_name == None:
						e_name = ""
					if desg == None:
						desg = ""
					if u_id == None:
						u_id = ""
					if no == None:
						no = ""
					html = """<html><head></head><body><p><b> Dear Client,</b><br/><br/>Greetings!<br/><br/>
					We thank you and confirm receipt of your email to quote for the above subject opportunity. Subject documents have been forwarded to our internal team for necessary action.<br/><br/>
					Thanking you,<br/><br/>
					Sincerely,<br/><br/>"""+e_name+""" <br/>"""+desg+"""<br/>"""+u_id+"""</br>"""+no+"""</p></body></html>"""
					frappe.sendmail(recipients = cust_email_id,
						cc = [self.bdm] ,
						subject=_("{0}/ Opportunity-{1}").format(self.name, self.project_name),
						message=_("""{0}""").format(html),
						reply_to= self.bdm)
				
				elif self.enquiry_from == "Customer" and self.customer is not None:
					#cust_email_id = frappe.db.get_value("Contact", {"Customer":self.customer}, "email_id")
					cust_email_id = frappe.db.get_value("Opportunity" , self.name , "contact_email")
					#frappe.msgprint(str(cust_email))
					e = frappe.db.get_value('Employee',{'user_id' : self.bdm}, ['employee_name', 'designation' , 'user_id' , 'cell_number'])
					#frappe.msgprint(str(e))
					e_name = str(e[0])
					desg = str(e[1])
					u_id = str(e[2])
					no = str(e[3])
					if no.startswith('0'):
						no=no.replace('0','+971 ')
						#frappe.msgprint(no)
					if '+971' not in no and no != None:
						no = '+971 ' + no
						#frappe.msgprint(no)
					if e_name == None:
						e_name = ""
					if desg == None:
						desg = ""
					if u_id == None:
						u_id = ""
					if no == None:
						no = ""
					html = """<html><head></head><body><p><b> Dear Client,</b><br/><br/>Greetings!<br/><br/>
					We thank you and confirm receipt of your email to quote for the above subject opportunity. Subject documents have been forwarded to our internal team for necessary action.<br/><br/>
					Thanking you,<br/><br/>
					Sincerely,<br/><br/>"""+e_name+""" <br/>"""+desg+"""<br/>"""+u_id+"""</br>"""+no+"""</p></body></html>"""
					frappe.sendmail(recipients = cust_email_id,
						subject=_("{0}/ Opportunity-{1}").format(self.name, self.project_name),
						cc = [self.bdm],
						message=_("""{0}""").format(html),
						reply_to= self.bdm)
			
				else:
					frappe.msgprint("not reached")
				
				val = 6
				self.notify_employee(cto, project_name, val, 1, customer_name)
				val = 1
				manager_rep = "ali@tablix.ae"
				task_sett = frappe.db.get_values('Commercial Task Settings',{'parent':'Buying Settings'}, ['module','upper_amount','lower_amount','tablix_rep'])
				for i in task_sett:
					if str(i[0]) == 'BOQ':
						manager_rep = str(i[3])
						break;
				self.notify_employee(manager_rep, project_name, val, 1, customer_name)
				#if type == "Security systems":
				#	self.notify_employee(security_engg1, project_name, val, 1, customer_name)
				#	self.notify_employee(security_engg2, project_name, val, 0, customer_name)
				#	self.notify_employee(security_engg3, project_name, val, 0, customer_name)
				#elif type == "Audio Visual":
				#	self.notify_employee(av_engg, project_name, val, 1, customer_name)
				#elif (type == "BMS" or type == "GRMS"):
				#	self.notify_employee(bms_engg, project_name, val, 1, customer_name)
				#else:
				#	self.notify_employee(ba_engg, project_name, val, 1, customer_name)
				val = 5
				self.notify_employee(opp_creator, project_name, val, 0, customer_name)
				if opp_creator == ceo or opp_creator == cbdo or opp_creator == coo:
					self.notify_employee(sales_coordinator, project_name, val, 0, customer_name)
			else:
				val = 0
				frappe.db.set_value("Opportunity", self.name, "status", "COO Approved")
				cur_date=datetime.datetime.now()
				cur_date = cur_date.strftime('%Y-%m-%d %H:%M:%S')
				frappe.db.set_value("Opportunity", self.name, "coo_date_time", cur_date)
				self.notify_employee(cbdo, project_name, val, 1, customer_name)
				val = 4
				self.notify_employee(opp_creator, project_name, val, 0, customer_name)
				if opp_creator == ceo or opp_creator == cbdo or opp_creator == coo:
					self.notify_employee(sales_coordinator, project_name, val, 0, customer_name)
				
		else:
			frappe.db.set_value("Opportunity", self.name, "status", "RFQ Approved")
			if self.enquiry_from == "Lead" and self.lead is not None:
				#cust_email_id = frappe.db.get_value("Lead", self.lead , "email_id")
				cust_email_id = frappe.db.get_value("Opportunity" , self.name , "contact_email")
				e = frappe.db.get_value('Employee',{'user_id' : self.bdm}, ['employee_name', 'designation' , 'user_id' , 'cell_number'])
				#frappe.msgprint(str(e))
				e_name = str(e[0])
				desg = str(e[1])
				u_id = str(e[2])
				no = str(e[3])
				if no.startswith('0'):
					no=no.replace('0','+971 ')
					#frappe.msgprint(no)
				if '+971' not in no and no != None:
					no = '+971 ' + no
					#frappe.msgprint(no)
				if e_name == None:
					e_name = ""
				if desg == None:
					desg = ""
				if u_id == None:
					u_id = ""
				if no == None:
					no = ""
				html = """<html><head></head><body><p><b> Dear Client,</b><br/><br/>Greetings!<br/><br/>
				We thank you and confirm receipt of your email to quote for the above subject opportunity. Subject documents have been forwarded to our internal team for necessary action.<br/><br/>
				Thanking you,<br/><br/>
				Sincerely,<br/><br/>"""+e_name+""" <br/>"""+desg+"""<br/>"""+u_id+"""</br>"""+no+"""</p></body></html>"""
				frappe.sendmail(recipients = cust_email_id,
					cc = [self.bdm],
					subject=_("{0}/ Opportunity-{1}").format(self.name, self.project_name),
					message=_("""{0}""").format(html),
					reply_to= self.bdm)
				
			elif self.enquiry_from == "Customer" and self.customer is not None:
				#cust_email_id = frappe.db.get_value("Contact", {"Customer":self.customer}, "email_id")
				cust_email_id = frappe.db.get_value("Opportunity" , self.name , "contact_email")
				#frappe.msgprint(str(cust_email))
				e = frappe.db.get_value('Employee',{'user_id' : self.bdm}, ['employee_name', 'designation' , 'user_id' , 'cell_number'])
				#frappe.msgprint(str(e))
				e_name = str(e[0])
				desg = str(e[1])
				u_id = str(e[2])
				no = str(e[3])
				if no.startswith('0'):
				    no=no.replace('0','+971 ')
					#frappe.msgprint(no)
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
				html = """<html><head></head><body><p><b> Dear Client,</b><br/><br/>Greetings!<br/><br/>
				We thank you and confirm receipt of your email to quote for the above subject opportunity. Subject documents have been forwarded to our internal team for necessary action.<br/><br/>
				Thanking you,<br/><br/>
				Sincerely,<br/><br/>"""+e_name+""" <br/>"""+desg+"""<br/>"""+u_id+"""</br>"""+no+"""</p></body></html>"""
				frappe.sendmail(recipients = cust_email_id,
					subject=_("{0}/ Opportunity-{1}").format(self.name, self.project_name),
					cc = [self.bdm],
					message=_("""{0}""").format(html),
					reply_to= self.bdm)
			
			else:
				frappe.msgprint("not reached")
						
			val = 6
			self.notify_employee(cto, project_name, val, 1, customer_name)
			val = 1
			manager_rep = "ali@tablix.ae"
			task_sett = frappe.db.get_values('Commercial Task Settings',{'parent':'Buying Settings'}, ['module','upper_amount','lower_amount','tablix_rep'])
			for i in task_sett:
				if str(i[0]) == 'BOQ':
					manager_rep = str(i[3])
					break;
			self.notify_employee(manager_rep, project_name, val, 1, customer_name)
			
			#if type == "Security systems":
			#	self.notify_employee(security_engg1, project_name, val, 1, customer_name)
			#	self.notify_employee(security_engg2, project_name, val, 0, customer_name)
			#	self.notify_employee(security_engg3, project_name, val, 0, customer_name)
			#elif type == "Audio Visual":
			#	self.notify_employee(av_engg, project_name, val, 1, customer_name)
			#elif type == "BMS":
			#	self.notify_employee(bms_engg, project_name, val, 1, customer_name)
			#else:
			#	self.notify_employee(ba_engg, project_name, val, 1, customer_name)
			val = 5
			self.notify_employee(opp_creator, project_name, val, 0, customer_name)
			if opp_creator == ceo or opp_creator == cbdo or opp_creator == coo:
					self.notify_employee(sales_coordinator, project_name, val, 0, customer_name)
			
		frappe.db.set_value("Opportunity", self.name, "prev_status", "")
		frappe.db.commit()
			
			
	def send_notification(self, reason):
		#msgprint("Entry: " + str(reason))
		if reason == "need_approval":
			#msgprint("need_approval")
			if self.prev_status:
				val = 3
			else:
				val = 0
			project_name = frappe.db.get_value("Opportunity", self.name, 'project_name')
			customer_name = frappe.db.get_value("Opportunity", self.name, 'customer_name')
			if self.prev_status == 'KAM Approved':
				self.notify_employee(coo, project_name, val, 1, customer_name)
				frappe.db.set_value("Opportunity", self.name, "prev_status", "")
				frappe.db.commit()		
			elif self.prev_status == 'COO Approved':
				self.notify_employee(cbdo, project_name, val, 1, customer_name)
				frappe.db.set_value("Opportunity", self.name, "prev_status", "")
				frappe.db.commit()		
			else:
				self.notify_employee(self.account_manager, project_name, val, 1, customer_name)
				frappe.db.set_value("Opportunity", self.name, "status", "RFQ")
				cur_date=datetime.datetime.now()
				cur_date = cur_date.strftime("%Y-%m-%d %H:%M:%S")
				frappe.db.set_value("Opportunity", self.name, "rfq_date_time", cur_date) 
				frappe.db.set_value("Opportunity", self.name, "prev_status", "")
				frappe.db.commit()
			
		elif reason == "need_info":
			
			val = 2
			#msgprint("need_info:" +  str(val))
			
			status = frappe.db.get_value("Opportunity", self.name, 'status')
			#msgprint("Status: " + status)
			project_name = frappe.db.get_value("Opportunity", self.name, 'project_name')
			opp_creator = frappe.db.get_value("Opportunity", self.name, 'bdm')
			customer_name = frappe.db.get_value("Opportunity", self.name, 'customer_name')
			if opp_creator == ceo or opp_creator == cbdo or opp_creator == coo:
				self.notify_employee(sales_coordinator, project_name, val, 1, customer_name)
				val = 7
				self.notify_employee(opp_creator, project_name, val, 0, customer_name)
			else:
				self.notify_employee(opp_creator, project_name, val, 1, customer_name)
			#frappe.db.set_value("Opportunity", self.name, "prev_status", self.status)
			#frappe.db.set_value("Opportunity", self.name, "status", "Insufficient Information");
		else:
			# ("added_info")
			val = 3
			project_name = frappe.db.get_value("Opportunity", self.name, 'project_name')
			type = frappe.db.get_value("Opportunity", self.name, 'type')
			customer_name = frappe.db.get_value("Opportunity", self.name, 'customer_name')
			frappe.db.set_value("Opportunity", self.name, "prev_status", "")
			self.notify_employee(cto, project_name, val, 1, customer_name)
			val = 1
			manager_rep = "ali@tablix.ae"
			task_sett = frappe.db.get_values('Commercial Task Settings',{'parent':'Buying Settings'}, ['module','upper_amount','lower_amount','tablix_rep'])
			for i in task_sett:
				if str(i[0]) == 'BOQ':
					manager_rep = str(i[3])
					break;
			self.notify_employee(manager_rep, project_name, val, 1, customer_name)
			#if type == "Security systems":
			#	self.notify_employee(security_engg1, project_name, val, 1, customer_name)
			#	self.notify_employee(security_engg2, project_name, val, 0, customer_name)
			#	self.notify_employee(security_engg3, project_name, val, 0, customer_name)
			#elif type == "Audio Visual":
			#	self.notify_employee(av_engg, project_name, val, 1, customer_name)
			#elif type == "BMS":
			#	self.notify_employee(bms_engg, project_name, val, 1, customer_name)
			#else:
			#	self.notify_employee(ba_engg, project_name, val, 1, customer_name)
	
			#frappe.db.set_value("Opportunity", self.name, "status", self.prev_status)
			frappe.db.commit()
		
		#frappe.db.set_value("Opportunity", self.name, "prev_status", "")
		
		return True
		
			
	def reopen(self):
		prev_status = frappe.db.get_value("Opportunity", self.name, 'prev_status')
		if prev_status == '' or prev_status is None:
			prev_status = 'Open'
		return prev_status	
			
			
	def notify_employee(self, employee, opp_subject, val, clear_val, customer): 
		
		
		#msgprint("Success" + str(val))
		
		def _get_message(url=False):
			if url:
				name = get_link_to_form(self.doctype, self.name)
			else:
				name = self.name
			if val == 0:
				return (_("Opportunity")+ "- %s of %s " + _("requires approval") + ": %s") % (opp_subject, customer, name)
			elif val == 1 or val == 6:
				return (_("Opportunity")+ "- %s of %s " + _("New request for BOQ creation") + ": %s") % (opp_subject, customer, name)
			elif val == 2:
				return (_("Opportunity")+ "- %s of %s " + _("does not contain sufficient information. Kindly provide") + ": %s") % (opp_subject, customer, name)
			elif val == 3:
				return (_("Opportunity")+ "- %s of %s " + _("added information. Kindly verify") + ": %s") % (opp_subject, customer, name)
			elif val == 4:
				return (_("Opportunity")+ "- %s of %s " + _("approved by Account Manager") + ": %s") % (opp_subject, customer, name)
			elif val == 5:
				return (_("Opportunity")+ "- %s of %s " + _("approved by CBDO") + ": %s") % (opp_subject, customer, name)
			elif val == 7:
				return (_("Opportunity")+ "- %s of %s " + _("does not contain sufficient information.") + ": %s") % (opp_subject, customer, name)
		
			
		self.notify({
			# for post in messages
			"message": _get_message(url=True),
			"message_to": employee,
			"subject": _get_message(),
		})
		
			
		if val ==0  or val ==1 or val ==2 or val == 3:
			proj_name = self.project_name.encode('ascii','ignore')
			if clear_val == 1:
				assign_to.clear(self.doctype, self.name)
			if val == 0:
				desc = "Opportunity for " + str(proj_name) + " requires Approval"
			elif val == 1:
				desc = "BOQ Request for Opportunity of " +str(proj_name)
			elif val == 2:
				desc = "Opportunity for " + str(proj_name) + " contains insufficient info"
			elif val == 3:
				desc = "Information added for " + str(proj_name) 
				#msgprint("assignment_addition")
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
		
		
def rfqtime():
	sql="""select name , account_manager , Date_Format(rfq_date_time , "%Y-%m-%d %H:%i:%s") As date , rfq_mail_sent from tabOpportunity where status = 'RFQ'"""
	var=frappe.db.sql(sql)
	#frappe.msgprint(str(var))
	for e in var:
		frappe.msgprint(str(e[0]))
		frappe.msgprint(str(e[2]))
		if e[2] is not None:
			frappe.msgprint("RFQ TIME")
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
			frappe.msgprint(str(hour_str))
			if hour_str != []:
				no_of_days = str(hour_str[0])
			#	msgprint(no_of_days)
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
					#	msgprint(str(total_hrs))
				#frappe.msgprint(str(e[3]))
				#frappe.msgprint("Hello")
				if total_hrs >= 2 and e[3]<=3:
					rm=int(e[3])
					rm = rm +1
					incr =int(rm)
					#frappe.msgprint(str(incr))
				elif total_hrs >= 2 and e[3]>3:
					incr = e[3]
				frappe.db.set_value("Opportunity", e[0], "rfq_mail_sent", incr)
				#frappe.msgprint("Updated")
				if total_hrs >= 2 and e[3]<=3:
					html = """<html><head></head><body><p>"""+ e[0] + """ is pending for Approval</p></body></html>"""
					frappe.sendmail(recipients = str(e[1]),
						subject=_("{0} is pending for Approvel").format(e[0]),
						message=_("""{0}""").format(html),
						reply_to= str(e[1]))
				elif total_hrs >= 2 and e[3] > 3:
					html = """<html><head></head><body><p>"""+ e[0] + """ is not approved by """ +final+ """ </p></body></html>"""
					frappe.sendmail(recipients = "gopu@tablix.ae",
						subject=_("{0} is pending for Approvel").format(e[0]),
						message=_("""{0}""").format(html),
						reply_to= "gopu@tablix.ae")
				else:
					frappe.msgprint("Email is not sent heigher person")

def kam_time():
	sql="""select name , account_manager , kam_date_time , kam_mail_sent from tabOpportunity where status = 'KAM Approved'"""
	var=frappe.db.sql(sql)
	#frappe.msgprint(str(var))
	for e in var:
		if e[2] is not None and e[2] != "":
			nm = []
			scnd =[]
			final = ""
			name = ""
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
					#	msgprint(str(total_hrs))
				else:
					no_of_hours = hour_str[0].split(":")
					if no_of_hours != []:
						hrs = float(no_of_hours[0]) *60*60
						mins = float(no_of_hours[1]) *60
						secs = float(no_of_hours[2])
						total_seconds = hrs + mins + secs
						total_hrs = total_seconds / 3600
					#	msgprint(str(total_hrs))
				#frappe.msgprint(str(e[3]))
				#frappe.msgprint("Hello")
				if total_hrs >= 2 and e[3]<=3:
					rm=int(e[3])
					rm = rm +1
					incr =int(rm)
					#frappe.msgprint(str(incr))
				elif total_hrs >= 2 and e[3]>3:
					incr = e[3]
				frappe.db.set_value("Opportunity", e[0], "kam_mail_sent", incr)
				#frappe.msgprint("Updated")
				if total_hrs >= 2 and e[3]<=3:
					html = """<html><head></head><body><p>"""+ e[0] + """ is pending for Approval</p></body></html>"""
					frappe.sendmail(recipients = str(coo),
						subject=_("{0} is pending for Approvel").format(e[0]),
						message=_("""{0}""").format(html),
						reply_to= str(coo))
				elif total_hrs >= 2 and e[3] > 3:
					html = """<html><head></head><body><p>"""+ e[0] + """ is not approved by """ +final+ """ </p></body></html>"""
					frappe.sendmail(recipients = "gopu@tablix.ae",
						subject=_("{0} is pending for Approvel").format(e[0]),
						message=_("""{0}""").format(html),
						reply_to= "gopu@tablix.ae")	
				else:
					frappe.msgprint("Email is not sent heigher person")		
					
	
			


@frappe.whitelist()
def get_item_details(item_code):
	item = frappe.db.sql("""select item_name, stock_uom, image, description, item_group, brand
		from `tabItem` where name = %s""", item_code, as_dict=1)
	return {
		'item_name': item and item[0]['item_name'] or '',
		'uom': item and item[0]['stock_uom'] or '',
		'description': item and item[0]['description'] or '',
		'image': item and item[0]['image'] or '',
		'item_group': item and item[0]['item_group'] or '',
		'brand': item and item[0]['brand'] or ''
	}

@frappe.whitelist()
def make_quotation(source_name, target_doc=None):
	def set_missing_values(source, target):
		quotation = frappe.get_doc(target)

		company_currency = frappe.db.get_value("Company", quotation.company, "default_currency")
		party_account_currency = get_party_account_currency("Customer", quotation.customer,
			quotation.company) if quotation.customer else company_currency

		quotation.currency = party_account_currency or company_currency

		if company_currency == quotation.currency:
			exchange_rate = 1
		else:
			exchange_rate = get_exchange_rate(quotation.currency, company_currency)

		quotation.conversion_rate = exchange_rate

		quotation.run_method("set_missing_values")
		quotation.run_method("calculate_taxes_and_totals")

	doclist = get_mapped_doc("Opportunity", source_name, {
		"Opportunity": {
			"doctype": "Quotation",
			"field_map": {
				"enquiry_from": "quotation_to",
				"enquiry_type": "order_type",
				"name": "enq_no",
			}
		},
		"Opportunity Item": {
			"doctype": "Quotation Item",
			"field_map": {
				"parent": "prevdoc_docname",
				"parenttype": "prevdoc_doctype",
				"uom": "stock_uom"
			},
			"add_if_empty": True
		}
	}, target_doc, set_missing_values)

	return doclist
	
	
@frappe.whitelist()
def make_boq(source_name, target_doc=None):
	boq = frappe.get_doc("Opportunity", source_name)
	#frappe.db.set_value("Opportunity", source_name, "status", "Boq")
	doclist = get_mapped_doc("Opportunity", source_name, {
		"Opportunity": {
			"doctype": "Boq",
			"field_map": {
				"account_manager": "account_manager",
				"name": "opportunity",
				"enquiry_from":"quotation_to",
				"lead":"lead",
				"customer":"customer",
				"project_name":"project_site_name",
				"solution":"system_type"
			}
		}
	})

	return doclist

@frappe.whitelist()
def set_multiple_status(names, status):
	names = json.loads(names)
	for name in names:
		opp = frappe.get_doc("Opportunity", name)
		opp.status = status
		opp.save()

		
