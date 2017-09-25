# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

class Course(Document):
<<<<<<< HEAD
	def validate(self):
		self.validate_assessment_criteria()
	
	def validate_assessment_criteria(self):
		if self.assessment_criteria:
			total_weightage = 0
			for criteria in self.assessment_criteria:
				total_weightage += criteria.weightage or 0
			if total_weightage != 100:
				frappe.throw(_("Total Weightage of all Assessment Criteria must be 100%"))
=======
	pass

def get_sg_list(doctype, txt, filters, limit_start, limit_page_length=20):
	user = frappe.session.user
	student = frappe.db.sql("select name from `tabStudent` where student_email_id= %s", user)
	if student:
		return frappe.db.sql('''select course, academic_term, academic_year, SG.name from `tabStudent Group`
			as SG, `tabStudent Group Student` as SGS where SG.name = SGS.parent and SGS.student = %s
			order by SG.name asc limit {0} , {1}'''.format(limit_start, limit_page_length), student, as_dict=True)

def get_list_context(context=None):
	return {
		"show_sidebar": True,
		'no_breadcrumbs': True,
		"title": _("Courses"),
		"get_list": get_sg_list,
		"row_template": "templates/includes/course/course_row.html"
	}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
