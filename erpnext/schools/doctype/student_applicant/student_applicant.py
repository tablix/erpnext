# -*- coding: utf-8 -*-777777yyy
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

<<<<<<< HEAD
from __future__ import print_function, unicode_literals
=======
from __future__ import unicode_literals
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
import frappe
from frappe import _
from frappe.model.document import Document

class StudentApplicant(Document):
<<<<<<< HEAD
	def autoname(self):
		from frappe.model.naming import set_name_by_naming_series
		if self.student_admission:
			naming_series = frappe.db.get_value('Student Admission', self.student_admission,
				'naming_series_for_student_applicant')
			print(naming_series)

			if naming_series:
				self.naming_series = naming_series

		set_name_by_naming_series(self)

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def validate(self):
		self.title = " ".join(filter(None, [self.first_name, self.middle_name, self.last_name]))

	def on_update_after_submit(self):
		student = frappe.get_list("Student",  filters= {"student_applicant": self.name})
		if student:
			frappe.throw(_("Cannot change status as student {0} is linked with student application {1}").format(student[0].name, self.name))
<<<<<<< HEAD

	def on_payment_authorized(self, *args, **kwargs):
		self.db_set('paid', 1)
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
