<<<<<<< HEAD
	# -*- coding: utf-8 -*-
=======
# -*- coding: utf-8 -*-
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
<<<<<<< HEAD
from frappe import _
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
from frappe.model.document import Document

class CourseSchedule(Document):
	def validate(self):
		self.instructor_name = frappe.db.get_value("Instructor", self.instructor, "instructor_name")
		self.set_title()
<<<<<<< HEAD
		self.validate_course()
		self.validate_date()
		self.validate_overlap()
	
	def set_title(self):
		"""Set document Title"""
		self.title = self.course + " by " + (self.instructor_name if self.instructor_name else self.instructor)
	
	def validate_course(self):
		group_based_on, course = frappe.db.get_value("Student Group", self.student_group, ["group_based_on", "course"])
		if group_based_on == "Course":
			self.course = course
=======
		self.validate_date()
		self.validate_overlap()
		
	def set_title(self):
		"""Set document Title"""
		self.title = self.course + " by " + (self.instructor_name if self.instructor_name else self.instructor)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	def validate_date(self):
		"""Validates if from_time is greater than to_time"""
		if self.from_time > self.to_time:
<<<<<<< HEAD
			frappe.throw(_("From Time cannot be greater than To Time."))
=======
			frappe.throw("From Time cannot be greater than To Time.")
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	
	def validate_overlap(self):
		"""Validates overlap for Student Group, Instructor, Room"""
		
		from erpnext.schools.utils import validate_overlap_for

<<<<<<< HEAD
		#Validate overlapping course schedules.
		if self.student_group:
			validate_overlap_for(self, "Course Schedule", "student_group")
		
		validate_overlap_for(self, "Course Schedule", "instructor")
		validate_overlap_for(self, "Course Schedule", "room")

		#validate overlapping assessment schedules.
		if self.student_group:
			validate_overlap_for(self, "Assessment Plan", "student_group")
		
		validate_overlap_for(self, "Assessment Plan", "room")
		validate_overlap_for(self, "Assessment Plan", "supervisor", self.instructor)
=======
		validate_overlap_for(self, "Course Schedule", "student_group" )
		validate_overlap_for(self, "Course Schedule", "instructor")
		validate_overlap_for(self, "Course Schedule", "room")

		validate_overlap_for(self, "Assessment", "student_group")
		validate_overlap_for(self, "Assessment", "room")
		validate_overlap_for(self, "Assessment", "supervisor", self.instructor)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

