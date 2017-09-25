# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
<<<<<<< HEAD
from frappe import _
from frappe.desk.form.linked_with import get_linked_doctypes

class Student(Document):
=======

class Student(Document):

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def validate(self):
		self.title = " ".join(filter(None, [self.first_name, self.middle_name, self.last_name]))

		if self.student_applicant:
			self.check_unique()
			self.update_applicant_status()

<<<<<<< HEAD
		if frappe.get_value("Student", self.name, "title") != self.title:
			self.update_student_name_in_linked_doctype()

	def update_student_name_in_linked_doctype(self):
		linked_doctypes = get_linked_doctypes("Student")
		for d in linked_doctypes:
			if "student_name" in [f.fieldname for f in frappe.get_meta(d).fields]:
				frappe.db.sql("""UPDATE `tab{0}` set student_name = %s where {1} = %s"""
					.format(d, linked_doctypes[d]["fieldname"]),(self.title, self.name))

			if "child_doctype" in linked_doctypes[d].keys() and "student_name" in \
				[f.fieldname for f in frappe.get_meta(linked_doctypes[d]["child_doctype"]).fields]:
				frappe.db.sql("""UPDATE `tab{0}` set student_name = %s where {1} = %s"""
					.format(linked_doctypes[d]["child_doctype"], linked_doctypes[d]["fieldname"]),(self.title, self.name))

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	def check_unique(self):
		"""Validates if the Student Applicant is Unique"""
		student = frappe.db.sql("select name from `tabStudent` where student_applicant=%s and name!=%s", (self.student_applicant, self.name))
		if student:
<<<<<<< HEAD
			frappe.throw(_("Student {0} exist against student applicant {1}").format(student[0][0], self.student_applicant))
=======
			frappe.throw("Student {0} exist against student applicant {1}".format(student[0][0], self.student_applicant))
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	def update_applicant_status(self):
		"""Updates Student Applicant status to Admitted"""
		if self.student_applicant:
			frappe.db.set_value("Student Applicant", self.student_applicant, "application_status", "Admitted")

def get_timeline_data(doctype, name):
	'''Return timeline for attendance'''
<<<<<<< HEAD
	return dict(frappe.db.sql('''select unix_timestamp(`date`), count(*)
		from `tabStudent Attendance` where
			student=%s
			and `date` > date_sub(curdate(), interval 1 year)
			and status = 'Present'
			group by date''', name))
=======
	return dict(frappe.db.sql('''select unix_timestamp(cs.schedule_date), count(*)
		from `tabCourse Schedule` as cs , `tabStudent Attendance` as sa where
			sa.course_schedule = cs.name
			and sa.student=%s
			and cs.schedule_date > date_sub(curdate(), interval 1 year)
			and status = 'Present'
			group by cs.schedule_date''', name))
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
