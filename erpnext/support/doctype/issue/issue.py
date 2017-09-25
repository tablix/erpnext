# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe import msgprint, _

from frappe.model.document import Document
from frappe.utils import now
from frappe.utils.user import is_website_user
from datetime import datetime

sender_field = "raised_by"

class Issue(Document):
	def get_feed(self):
		return "{0}: {1}".format(_(self.status), self.subject)

	def validate(self):
		if not self.raised_by:
			self.raised_by = frappe.session.user
		self.update_status()
		self.set_lead_contact(self.raised_by)

		if self.status == "Closed":
			from frappe.desk.form.assign_to import clear
			clear(self.doctype, self.name)
		self.update_status()

	def set_lead_contact(self, email_id):
		import email.utils
		email_id = email.utils.parseaddr(email_id)[1]
		if email_id:
			if not self.lead:
				self.lead = frappe.db.get_value("Lead", {"email_id": email_id})
			if not self.contact:
				values = frappe.db.get_value("Contact",
					{"email_id": email_id}, ("name", "customer"))

				if values:
					self.contact, self.customer = values

			if not self.company:
				self.company = frappe.db.get_value("Lead", self.lead, "company") or \
					frappe.db.get_default("Company")

	def update_status(self):
		status = frappe.db.get_value("Issue", self.name, "status")
		#if self.status!="Open" and status =="Open" and not self.first_responded_on:
		#	self.first_responded_on = now()
		#if self.status=="Closed" and status !="Closed":
		#	self.resolution_date = now()
		#if self.status=="Open" and status !="Open":
			# if no date, it should be set as None and not a blank string "", as per mysql strict config
		#	self.resolution_date = None
		if self.status == "Attended" and status == "Open":
			self.attended_datetime = now()
		if self.status =="Closed":
			self.date_time_closed = now()
			opening_datetime = self.opening_date + ' ' + self.opening_time
			#msgprint(_("Opening Datetime: {0}").format(opening_datetime))
			#msgprint(_("Now Datetime: {0}").format(now()))
			fmt = '%Y-%m-%d %H:%M:%S'
			d0 = datetime.strptime(opening_datetime, fmt)
			d1 = now()
			#msgprint(_("d1: {0}").format(d1))
			d1 = d1.rsplit('.',1)[0]
			#msgprint(_("d0: {0}, d1: {1}").format(d0,d1))
			d1 = datetime.strptime(d1, fmt)
			self.time_duration_ = (d1-d0).total_seconds()
			#msgprint(_("Time Duration: {0}").format(self.time_duration_))
			self.time_duration_ = (d1-d0).total_seconds()/60
			#msgprint(_("Time Duration: {0}").format(self.time_duration_))
			if self.attended_datetime is not None and self.attended_datetime != '':
				if self.rectification_datetime is not None and self.rectification_datetime != '':
					d2 = datetime.strptime(self.rectification_datetime, fmt)
					d3 = datetime.strptime(self.attended_datetime, fmt)
					rectification_time = (d2-d3).total_seconds()/60
					#msgprint(_("Rectification Time Duration: {0}").format(str(rectification_time)))
					rectification_time_hr_ = rectification_time / 60
					self.rectification_time = rectification_time_hr_
					#msgprint(_("Rectification Time Duration: {0}").format(str(rectification_time_hr_)))
					rectification_time_hr_new = str(rectification_time_hr_)
					rectification_time_hr_0 = rectification_time_hr_new.split('.')[0]
					rectification_time_hr_1 = rectification_time_hr_new.split('.')[1]
					if int(rectification_time_hr_1) > 0:
						rectification_time_hr = int(rectification_time_hr_0) + 1
					else: 
						rectification_time_hr = int(rectification_time_hr_0)
					#msgprint(_("Rectification Time Duration: {0}").format(str(rectification_time_hr)))
					if int(rectification_time_hr) <= 0:
						self.rectification_time_duration = '0'
					if int(rectification_time_hr) >0 and int(rectification_time_hr) < 2:
						self.rectification_time_duration = '0-2'
					elif int(rectification_time_hr) >= 2 and int(rectification_time_hr) < 4:
						self.rectification_time_duration = '2-4'
					elif int(rectification_time_hr) >= 4 and int(rectification_time_hr) < 8:
						self.rectification_time_duration = '4-8'
					elif int(rectification_time_hr) >= 8 and int(rectification_time_hr) < 12:
						self.rectification_time_duration = '8-12'
					elif int(rectification_time_hr) >= 12 and int(rectification_time_hr) < 16:
						self.rectification_time_duration = '12-16'
					elif int(rectification_time_hr) >= 16 and int(rectification_time_hr) < 20:
						self.rectification_time_duration = '16-20'
					elif int(rectification_time_hr) >= 20 and int(rectification_time_hr) <= 24:
						self.rectification_time_duration = '20-24'
					elif int(rectification_time_hr) > 24 and int(rectification_time_hr) < 48:
						self.rectification_time_duration = 'More than 1 day'
					elif int(rectification_time_hr) >= 48 and int(rectification_time_hr) <= 72:
						self.rectification_time_duration = 'More than 2 day'
					elif int(rectification_time_hr) > 72 :
						self.rectification_time_duration = 'More than 72 hrs'
		
					#msgprint(_("Rectification Time: {0}").format(self.rectification_time_duration))
			else:
				msgprint(_("Warning:Attended Status was not selected so Rectification Time Duration was not calculated"))
			
	
			
			

def get_list_context(context=None):
	return {
		"title": _("Issues"),
		"get_list": get_issue_list,
		"row_template": "templates/includes/issue_row.html",
		"show_sidebar": True,
		"show_search": True,
		'no_breadcrumbs': True
	}

def get_issue_list(doctype, txt, filters, limit_start, limit_page_length=20):
	from frappe.www.list import get_list
	user = frappe.session.user
	ignore_permissions = False
	if is_website_user():
		if not filters: filters = []
		filters.append(("Issue", "raised_by", "=", user))
		ignore_permissions = True

	return get_list(doctype, txt, filters, limit_start, limit_page_length, ignore_permissions=ignore_permissions)

@frappe.whitelist()
def set_status(name, status):
	st = frappe.get_doc("Issue", name)
	st.status = status
	st.save()

def auto_close_tickets():
	frappe.db.sql("""update `tabIssue` set status = 'Closed'
		where status = 'Replied'
		and date_sub(curdate(),interval 15 Day) > modified""")

@frappe.whitelist()
def set_multiple_status(names, status):
	names = json.loads(names)
	for name in names:
		set_status(name, status)

def has_website_permission(doc, ptype, user, verbose=False):
	return doc.raised_by==user
