# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

from frappe.utils import getdate, validate_email_add, today, add_years
from frappe.model.naming import make_autoname
from frappe import throw, _
import frappe.permissions
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from erpnext.utilities.transaction_base import delete_events

from calendar import monthrange
import datetime 


class EmployeeUserDisabledError(frappe.ValidationError):
	pass


class Employee(Document):
	def autoname(self):
		naming_method = frappe.db.get_value("HR Settings", None, "emp_created_by")
		if not naming_method:
			throw(_("Please setup Employee Naming System in Human Resource > HR Settings"))
		else:
			if naming_method == 'Naming Series':
				self.name = make_autoname(self.naming_series + '.####')
			elif naming_method == 'Employee Number':
				self.name = self.employee_number

		self.employee = self.name

	def validate(self):
		from erpnext.controllers.status_updater import validate_status
		validate_status(self.status, ["Active", "Left"])

		self.employee = self.name
		self.validate_date()
		self.validate_email()
		self.validate_status()
		self.validate_employee_leave_approver()
		self.validate_reports_to()
		#exp_doc()

		if self.user_id:
			self.validate_for_enabled_user_id()
			self.validate_duplicate_user_id()
		else:
			existing_user_id = frappe.db.get_value("Employee", self.name, "user_id")
			if existing_user_id:
				frappe.permissions.remove_user_permission(
					"Employee", self.name, existing_user_id)

	def on_update(self):
		# add allocated & balance leaves			
		doj=str(self.date_of_joining)
		doj=datetime.datetime.strptime(doj, "%Y-%m-%d")
		d2=datetime.datetime.strptime(today(),"%Y-%m-%d")
		delta = 0
		while True:
			mdays = monthrange(doj.year, doj.month)[1]
			doj += datetime.timedelta(days=mdays)
			if doj <= d2:
				delta += 1
			else:
				break
				
		leaves_alloc = delta*2.5
		self.total_leaves_allocated = leaves_alloc
		self.balance_leave = leaves_alloc - self.total_leaves_consumed
		frappe.db.set_value("Employee", self.employee, "total_leaves_allocated" , self.total_leaves_allocated)
		frappe.db.set_value("Employee", self.employee, "total_leaves_consumed" , self.total_leaves_consumed)
		frappe.db.set_value("Employee", self.employee, "balance_leave", self.balance_leave)
		frappe.db.commit()	
		
		if self.user_id:
			self.update_user()
			self.update_user_permissions()

	def update_user_permissions(self):
		frappe.permissions.add_user_permission("Employee", self.name, self.user_id)
		frappe.permissions.set_user_permission_if_allowed("Company", self.company, self.user_id)

	def update_user(self):
		# add employee role if missing
		user = frappe.get_doc("User", self.user_id)
		user.flags.ignore_permissions = True

		if "Employee" not in user.get("user_roles"):
			user.add_roles("Employee")

		# copy details like Fullname, DOB and Image to User
		if self.employee_name and not (user.first_name and user.last_name):
			employee_name = self.employee_name.split(" ")
			if len(employee_name) >= 3:
				user.last_name = " ".join(employee_name[2:])
				user.middle_name = employee_name[1]
			elif len(employee_name) == 2:
				user.last_name = employee_name[1]

			user.first_name = employee_name[0]

		if self.date_of_birth:
			user.birth_date = self.date_of_birth

		if self.gender:
			user.gender = self.gender

		if self.image:
			if not user.user_image:
				user.user_image = self.image
				try:
					frappe.get_doc({
						"doctype": "File",
						"file_name": self.image,
						"attached_to_doctype": "User",
						"attached_to_name": self.user_id
					}).insert()
				except frappe.DuplicateEntryError:
					# already exists
					pass

		
		user.save()

	def validate_date(self):
		if self.date_of_birth and getdate(self.date_of_birth) > getdate(today()):
			throw(_("Date of Birth cannot be greater than today."))

		if self.date_of_birth and self.date_of_joining and getdate(self.date_of_birth) >= getdate(self.date_of_joining):
			throw(_("Date of Joining must be greater than Date of Birth"))

		elif self.date_of_retirement and self.date_of_joining and (getdate(self.date_of_retirement) <= getdate(self.date_of_joining)):
			throw(_("Date Of Retirement must be greater than Date of Joining"))

		elif self.relieving_date and self.date_of_joining and (getdate(self.relieving_date) <= getdate(self.date_of_joining)):
			throw(_("Relieving Date must be greater than Date of Joining"))

		elif self.contract_end_date and self.date_of_joining and (getdate(self.contract_end_date) <= getdate(self.date_of_joining)):
			throw(_("Contract End Date must be greater than Date of Joining"))

	def validate_email(self):
		if self.company_email:
			validate_email_add(self.company_email, True)
		if self.personal_email:
			validate_email_add(self.personal_email, True)

	def validate_status(self):
		if self.status == 'Left' and not self.relieving_date:
			throw(_("Please enter relieving date."))

	def validate_for_enabled_user_id(self):
		if not self.status == 'Active':
			return
		enabled = frappe.db.get_value("User", self.user_id, "enabled")
		if enabled is None:
			frappe.throw(_("User {0} does not exist").format(self.user_id))
		if enabled == 0:
			frappe.throw(_("User {0} is disabled").format(self.user_id), EmployeeUserDisabledError)

	def validate_duplicate_user_id(self):
		employee = frappe.db.sql_list("""select name from `tabEmployee` where
			user_id=%s and status='Active' and name!=%s""", (self.user_id, self.name))
		if employee:
			throw(_("User {0} is already assigned to Employee {1}").format(
				self.user_id, employee[0]), frappe.DuplicateEntryError)

	def validate_employee_leave_approver(self):
		for l in self.get("leave_approvers")[:]:
			if "Leave Approver" not in frappe.get_roles(l.leave_approver):
				frappe.get_doc("User", l.leave_approver).add_roles("Leave Approver")

	def validate_reports_to(self):
		if self.reports_to == self.name:
			throw(_("Employee cannot report to himself."))

	def on_trash(self):
		delete_events(self.doctype, self.name)

def get_timeline_data(doctype, name):
	'''Return timeline for attendance'''
	return dict(frappe.db.sql('''select unix_timestamp(att_date), count(*)
		from `tabAttendance` where employee=%s
			and att_date > date_sub(curdate(), interval 1 year)
			and status in ('Present', 'Half Day')
			group by att_date''', name))

@frappe.whitelist()
def get_retirement_date(date_of_birth=None):
	import datetime
	ret = {}
	if date_of_birth:
		try:
			retirement_age = int(frappe.db.get_single_value("HR Settings", "retirement_age") or 60)
			dt = add_years(getdate(date_of_birth),retirement_age)
			ret = {'date_of_retirement': dt.strftime('%Y-%m-%d')}
		except ValueError:
			# invalid date
			ret = {}

	return ret


@frappe.whitelist()
def make_salary_structure(source_name, target=None):
	target = get_mapped_doc("Employee", source_name, {
		"Employee": {
			"doctype": "Salary Structure",
			"field_map": {
				"name": "employee",
			}
		}
	})
	target.make_earn_ded_table()
	return target

def validate_employee_role(doc, method):
	# called via User hook
	if "Employee" in [d.role for d in doc.get("user_roles")]:
		if not frappe.db.get_value("Employee", {"user_id": doc.name}):
			frappe.msgprint(_("Please set User ID field in an Employee record to set Employee Role"))
			doc.get("user_roles").remove(doc.get("user_roles", {"role": "Employee"})[0])

def update_user_permissions(doc, method):
	# called via User hook
	if "Employee" in [d.role for d in doc.get("user_roles")]:
		employee = frappe.get_doc("Employee", {"user_id": doc.name})
		employee.update_user_permissions()

def send_birthday_reminders():
	"""Send Employee birthday reminders if no 'Stop Birthday Reminders' is not set."""
	if int(frappe.db.get_single_value("HR Settings", "stop_birthday_reminders") or 0):
		return

	from frappe.utils.user import get_enabled_system_users
	users = None

	birthdays = get_employees_who_are_born_today()

	if birthdays:
		if not users:
			users = [u.email_id or u.name for u in get_enabled_system_users()]

		for e in birthdays:
			frappe.sendmail(recipients=filter(lambda u: u not in (e.company_email, e.personal_email, e.user_id), users),
				subject=_("Birthday Reminder for {0}").format(e.employee_name),
				message=_("""Today is {0}'s birthday!""").format(e.employee_name),
				reply_to=e.company_email or e.personal_email or e.user_id)
				
def send_passport_expiry_reminders():
	"""Send Employee Passport Expiry reminders."""
	
	from frappe.utils.user import get_enabled_system_users
	users = None
	expiry_date = get_passport_expiry()
	frappe.msgprint(expiry_date);
	html = ""
	e = []
	if expiry_date:
		html = """\
				<html>
  					<head></head>
  						<body>"""
		for e in expiry_date:
			html += """<p>"""+ e[0] + """ 's Passport going to expire on """ + e[1]+ """</p>"""
    	html += """</body></html>"""
    	if e is not None and e != []:
    		month = datetime.datetime.strptime(e[1],"%Y-%m-%d")
    		month = month.strftime("%B")
    		frappe.sendmail(recipients = "anushree.gireeshkumar@tablix.ae",
				subject=_("Passport Expiry Reminder for the Month of {0}").format(month),
				message=_("""{0}""").format(html),
				reply_to= "anushree.gireeshkumar@tablix.ae")
				
	
		
def get_passport_expiry():
	cur_date=datetime.datetime.now()
	curr_month = cur_date.strftime("%m")
	#frappe.msgprint(curr_month)
	if curr_month != "10" :
		curr_month = curr_month.replace("0","")
		#frappe.msgprint(curr_month)
	next_month = int(curr_month) + 1
	days=monthrange(cur_date.year,next_month)
	from_date = datetime.date(cur_date.year,next_month,1)
	to_date =  datetime.date(cur_date.year,next_month,days[1])
	from_date=from_date.strftime("%Y-%m-%d")
	#frappe.msgprint("current date " + from_date)
	to_date=to_date.strftime("%Y-%m-%d")
	#frappe.msgprint("next date " + to_date)
	return frappe.db.sql("""select employee_name , DATE_FORMAT(valid_upto, '%%Y-%%m-%%d') AS date , user_id from `tabEmployee` where valid_upto >= '2017-07-01' and valid_upto <= %s""",(to_date))
    	

def send_labour_card_expiry_reminders():
	"""Send Employee Labour Card Expiry reminders."""
	
	from frappe.utils.user import get_enabled_system_users
	users = None
	expiry_date = get_labour_card_expiry()
	frappe.msgprint(expiry_date);
	html = ""
	e = []
	if expiry_date:
		html = """\
				<html>
  					<head></head>
  						<body>"""
		for e in expiry_date:
			html += """<p>"""+ e[0] + """ 's Labour Card going to expire on """ + e[1]+ """</p>"""
    	html += """</body></html>"""
    	if e is not None and e != []:
    		month = datetime.datetime.strptime(e[1],"%Y-%m-%d")
    		month = month.strftime("%B")
    		frappe.sendmail(recipients = "anushree.gireeshkumar@tablix.ae",
				subject=_("Labour Card Expiry Reminder for {0}").format(month),
				message=_("""{0}""").format(html),
				reply_to= "anushree.gireeshkumar@tablix.ae")
				
		
def get_labour_card_expiry():
	#curr_date = datetime.date.today().isoformat()
	cur_date=datetime.datetime.now()
	curr_month = cur_date.strftime("%m")
	#frappe.msgprint(curr_month)
	if curr_month != "10" :
		curr_month = curr_month.replace("0","")
		#frappe.msgprint(curr_month)
	next_month = int(curr_month) + 1
	days=monthrange(cur_date.year,next_month)
	from_date = datetime.date(cur_date.year,next_month,1)
	to_date =  datetime.date(cur_date.year,next_month,days[1])
	from_date=from_date.strftime("%Y-%m-%d")
	#frappe.msgprint("current date " + from_date)
	to_date=to_date.strftime("%Y-%m-%d")
	#frappe.msgprint("next date " + to_date)
	return frappe.db.sql("""select employee_name , DATE_FORMAT(labour_card_expiry_date, '%%Y-%%m-%%d') AS date , user_id from `tabEmployee` where labour_card_expiry_date >= '2017-07-01' and labour_card_expiry_date <= %s""",( to_date))
   
def send_e_id_expiry_reminders():
	"""Send Employee Emirates Id Expiry reminders."""
	
	from frappe.utils.user import get_enabled_system_users
	users = None
	expiry_date = get_e_id_expiry()
	frappe.msgprint(expiry_date);
	html = ""
	e = []
	if expiry_date:
		html = """\
				<html>
  					<head></head>
  						<body>"""
		for e in expiry_date:
			html += """<p>"""+ e[0] + """ 's Emirates Id going to expire on """ + e[1]+ """</p>"""
    	html += """</body></html>"""
    	if e is not None and e != []:
    		month = datetime.datetime.strptime(e[1],"%Y-%m-%d")
    		month = month.strftime("%B")
    		frappe.sendmail(recipients = "anushree.gireeshkumar@tablix.ae",
				subject=_("Emirates Id Expiry Reminder for {0}").format(month),
				message=_("""{0}""").format(html),
				reply_to= "anushree.gireeshkumar@tablix.ae")
				
		
def get_e_id_expiry():
	#curr_date = datetime.date.today().isoformat()
	cur_date=datetime.datetime.now()
	curr_month = cur_date.strftime("%m")
	#frappe.msgprint(curr_month)
	if curr_month != "10" :
		curr_month = curr_month.replace("0","")
		#frappe.msgprint(curr_month)
	next_month = int(curr_month) + 1
	days=monthrange(cur_date.year,next_month)
	from_date = datetime.date(cur_date.year,next_month,1)
	to_date =  datetime.date(cur_date.year,next_month,days[1])
	from_date=from_date.strftime("%Y-%m-%d")
	#frappe.msgprint("current date " + from_date)
	to_date=to_date.strftime("%Y-%m-%d")
	#frappe.msgprint("next date " + to_date)
	return frappe.db.sql("""select employee_name , DATE_FORMAT(eid_expiry, '%%Y-%%m-%%d') AS date , user_id from `tabEmployee` where eid_expiry >= '2017-07-01' and eid_expiry <= %s""",( to_date))
   
def send_visa_expiry_reminders():
	"""Send Employee Visa Expiry reminders."""
	
	from frappe.utils.user import get_enabled_system_users
	users = None
	expiry_date = get_visa_expiry()
	frappe.msgprint(expiry_date);
	html = ""
	e = []
	if expiry_date:
		html = """\
				<html>
  					<head></head>
  						<body>"""
		for e in expiry_date:
			html += """<p>"""+ e[0] + """ 's Visa going to expire on """ + e[1]+ """</p>"""
    	html += """</body></html>"""
    	if e is not None and e != []:
    		month = datetime.datetime.strptime(e[1],"%Y-%m-%d")
    		month = month.strftime("%B")
    		frappe.sendmail(recipients = "anushree.gireeshkumar@tablix.ae",
				subject=_("Visa Expiry Reminder for {0}").format(month),
				message=_("""{0}""").format(html),
				reply_to= "anushree.gireeshkumar@tablix.ae")
				
		
def get_visa_expiry():
	#curr_date = datetime.date.today().isoformat()
	cur_date=datetime.datetime.now()
	curr_month = cur_date.strftime("%m")
	#frappe.msgprint(curr_month)
	if curr_month != "10" :
		curr_month = curr_month.replace("0","")
		#frappe.msgprint(curr_month)
	next_month = int(curr_month) + 1
	days=monthrange(cur_date.year,next_month)
	from_date = datetime.date(cur_date.year,next_month,1)
	to_date =  datetime.date(cur_date.year,next_month,days[1])
	from_date=from_date.strftime("%Y-%m-%d")
	#frappe.msgprint("current date " + from_date)
	to_date=to_date.strftime("%Y-%m-%d")
	#frappe.msgprint("next date " + to_date)
	return frappe.db.sql("""select employee_name , DATE_FORMAT(visa_expiry, '%%Y-%%m-%%d') AS date , user_id from `tabEmployee` where visa_expiry >= '2017-07-01' and visa_expiry <= %s""",( to_date))
   
def send_health_card_reminders():
	"""Send Employee HealthCard Expiry reminders."""
	
	from frappe.utils.user import get_enabled_system_users
	users = None
	expiry_date = get_health_card_expiry()
	frappe.msgprint(expiry_date);
	html = ""
	e = []
	if expiry_date:
		html = """\
				<html>
  					<head></head>
  						<body>"""
		for e in expiry_date:
			html += """<p>"""+ e[0] + """ 's Health Card going to expire on """ + e[1]+ """</p>"""
    	html += """</body></html>"""
    	if e is not None and e != []:
    		month = datetime.datetime.strptime(e[1],"%Y-%m-%d")
    		month = month.strftime("%B")
    		frappe.sendmail(recipients = "anushree.gireeshkumar@tablix.ae",
				subject=_("Health Card Expiry Reminder for {0}").format(month),
				message=_("""{0}""").format(html),
				reply_to= "anushree.gireeshkumar@tablix.ae")
				
		
def get_health_card_expiry():
	#curr_date = datetime.date.today().isoformat()
	cur_date=datetime.datetime.now()
	curr_month = cur_date.strftime("%m")
	#frappe.msgprint(curr_month)
	if curr_month != "10" :
		curr_month = curr_month.replace("0","")
		#frappe.msgprint(curr_month)
	next_month = int(curr_month) + 1
	days=monthrange(cur_date.year,next_month)
	from_date = datetime.date(cur_date.year,next_month,1)
	to_date =  datetime.date(cur_date.year,next_month,days[1])
	from_date=from_date.strftime("%Y-%m-%d")
	#frappe.msgprint("current date " + from_date)
	to_date=to_date.strftime("%Y-%m-%d")
	#frappe.msgprint("next date " + to_date)
	return frappe.db.sql("""select employee_name , DATE_FORMAT(expiry_date, '%%Y-%%m-%%d') AS date , user_id from `tabEmployee` where expiry_date >= '2017-07-01' and expiry_date <= %s""",(to_date))
   
   
def send_vehicle_insurance_expiry_reminders():
	"""Send Employee Vehicle Insurance Expiry reminders."""
	
	from frappe.utils.user import get_enabled_system_users
	users = None
	expiry_date = get_vehicle_insurance_expiry()
	frappe.msgprint(expiry_date);
	html = ""
	e = []
	if expiry_date:
		html = """\
				<html>
  					<head></head>
  						<body>"""
		for e in expiry_date:
			html += """<p>"""+ e[0] + """ 's Vehicle No.""" + e[2]+ """ Insurance going to expire on """ + e[1]+ """</p>"""
    	html += """</body></html>"""
    	if e is not None and e != []:
    		month = datetime.datetime.strptime(e[1],"%Y-%m-%d")
    		month = month.strftime("%B")
    		frappe.sendmail(recipients = "anushree.gireeshkumar@tablix.ae",
				subject=_("Vehicle Insurance Expiry Reminder for {0}").format(month),
				message=_("""{0}""").format(html),
				reply_to= "anushree.gireeshkumar@tablix.ae")
				
		
def get_vehicle_insurance_expiry():
	cur_date=datetime.datetime.now()
	curr_month = cur_date.strftime("%m")
	#frappe.msgprint(curr_month)
	if curr_month != "10" :
		curr_month = curr_month.replace("0","")
		#frappe.msgprint(curr_month)
	next_month = int(curr_month) + 1
	days=monthrange(cur_date.year,next_month)
	from_date = datetime.date(cur_date.year,next_month,1)
	to_date =  datetime.date(cur_date.year,next_month,days[1])
	from_date=from_date.strftime("%Y-%m-%d")
	#frappe.msgprint("current date " + from_date)
	to_date=to_date.strftime("%Y-%m-%d")
	#frappe.msgprint("next date " + to_date)
	return frappe.db.sql("""select emp_name ,  DATE_FORMAT(insurance_exp, '%%Y-%%m-%%d') AS date , IFNULL(vehicle_number, ""	) from `tabVehicle Detail` where insurance_exp >= '2017-07-01' and insurance_exp <= %s""",(to_date))


def exp_doc():
	passport_date = get_passport_expiry()
	#frappe.msgprint(passport_date)
	
	labour_card_date = get_labour_card_expiry()
	#frappe.msgprint(labour_card_date);
	e_id_date = get_e_id_expiry()
	#frappe.msgprint(e_id_date);
	visa_date = get_visa_expiry()
	#frappe.msgprint(visa_date);
	health_card_date = get_health_card_expiry()
	#frappe.msgprint(health_card_date);
	
	vehicle_date = get_vehicle_insurance_expiry()
	#frappe.msgprint(vehicle_date);
	
	html = """<html><head><style>
table, th, td {
    border: 1px solid black;
}
</style></head><body><table style="width:100%"><tr><th>Type</th><th>Employee Name </th><th>Expiry Date</th><th>Days Remaining</th><th>Vehicle No.</th></tr>"""
	e = []
	for e in passport_date:
		fmt = '%Y-%m-%d'
		exp_date = datetime.datetime.strptime(e[1], fmt)
		exp_date = datetime.datetime.strftime(exp_date, fmt)
		date2 = datetime.datetime.now()
		date2 = datetime.datetime.strftime(date2, fmt)
		datediff = frappe.utils.data.time_diff(exp_date, date2)
		datediff = datediff.__str__()
		html += """<tr><td>Passport</td><td>"""+e[0]+"""</td><td>"""+e[1]+"""</td><td>"""+datediff+"""</td><td></td></tr>"""
					
	for e in labour_card_date:
		fmt = '%Y-%m-%d'
		exp_date = datetime.datetime.strptime(e[1], fmt)
		exp_date = datetime.datetime.strftime(exp_date, fmt)
		date2 = datetime.datetime.now()
		date2 = datetime.datetime.strftime(date2, fmt)
		datediff = frappe.utils.data.time_diff(exp_date, date2)
		datediff = datediff.__str__()
		html += """<tr><td>Labour Card</td><td>"""+e[0]+"""</td><td>"""+e[1]+"""</td><td>"""+datediff+"""</td><td></td></tr>"""
	
		
  	for e in e_id_date:
		fmt = '%Y-%m-%d'
		exp_date = datetime.datetime.strptime(e[1], fmt)
		exp_date = datetime.datetime.strftime(exp_date, fmt)
		date2 = datetime.datetime.now()
		date2 = datetime.datetime.strftime(date2, fmt)
		datediff = frappe.utils.data.time_diff(exp_date, date2)
		datediff = datediff.__str__()
		html += """<tr><td>Emirates Id</td><td>"""+e[0]+"""</td><td>"""+e[1]+"""</td><td>"""+datediff+"""</td><td></td></tr>"""	
  
  	for e in visa_date:
		fmt = '%Y-%m-%d'
		exp_date = datetime.datetime.strptime(e[1], fmt)
		exp_date = datetime.datetime.strftime(exp_date, fmt)
		date2 = datetime.datetime.now()
		date2 = datetime.datetime.strftime(date2, fmt)
		datediff = frappe.utils.data.time_diff(exp_date, date2)
		datediff = datediff.__str__()
		html += """<tr><td>Visa</td><td>"""+e[0]+"""</td><td>"""+e[1]+"""</td><td>"""+datediff+"""</td><td></td></tr>"""
 
 	for e in health_card_date:
		fmt = '%Y-%m-%d'
		exp_date = datetime.datetime.strptime(e[1], fmt)
		exp_date = datetime.datetime.strftime(exp_date, fmt)
		date2 = datetime.datetime.now()
		date2 = datetime.datetime.strftime(date2, fmt)
		datediff = frappe.utils.data.time_diff(exp_date, date2)
		datediff = datediff.__str__()
		html += """<tr><td>Health Card</td><td>"""+e[0]+"""</td><td>"""+e[1]+"""</td><td>"""+datediff+"""</td><td></td></tr>"""
		
	for e in vehicle_date:
		fmt = '%Y-%m-%d'
		exp_date = datetime.datetime.strptime(e[1], fmt)
		exp_date = datetime.datetime.strftime(exp_date, fmt)
		date2 = datetime.datetime.now()
		date2 = datetime.datetime.strftime(date2, fmt)
		datediff = frappe.utils.data.time_diff(exp_date, date2)
		datediff = datediff.__str__()
		html += """<tr><td>Vehicle Insurance</td><td>"""+e[0]+"""</td><td>"""+e[1]+"""</td><td>"""+datediff+"""</td><td>"""+e[2]+"""</td></tr>"""
  		
	if e is not None and e != []:
		html += """</table></body></html>"""
		month = datetime.datetime.strptime(e[1],"%Y-%m-%d")
		month = month.strftime("%B")
		#frappe.sendmail(recipients = ("anushree.gireeshkumar@tablix.ae","varna.manoj@tablix.ae","deepak.agarwal@tablix.ae"),
		frappe.sendmail(recipients = "anushree.gireeshkumar@tablix.ae",
			subject=_("Document Expiry Reminder for {0}").format(month),
			message=_("""{0}""").format(html),
			reply_to= "anushree.gireeshkumar@tablix.ae")			






def get_employees_who_are_born_today():
	"""Get Employee properties whose birthday is today."""
	return frappe.db.sql("""select name, personal_email, company_email, user_id, employee_name
		from tabEmployee where day(date_of_birth) = day(%(date)s)
		and month(date_of_birth) = month(%(date)s)
		and status = 'Active'""", {"date": today()}, as_dict=True)

def get_holiday_list_for_employee(employee, raise_exception=True):
	holiday_list, company = frappe.db.get_value("Employee", employee, ["holiday_list", "company"])

	if not holiday_list:
		holiday_list = frappe.db.get_value("Company", company, "default_holiday_list")

	if not holiday_list and raise_exception:
		frappe.throw(_('Please set a default Holiday List for Employee {0} or Company {1}').format(employee, company))

	return holiday_list

