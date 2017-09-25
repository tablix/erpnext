# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
<<<<<<< HEAD
from frappe import msgprint, _
from frappe.model.document import Document

class AcademicYear(Document):
    def validate(self):
        #Check that start of academic year is earlier than end of academic year
        if self.year_start_date and self.year_end_date and self.year_start_date > self.year_end_date:
            frappe.throw(_("The Year End Date cannot be earlier than the Year Start Date. Please correct the dates and try again."))
=======
from frappe.model.document import Document

class AcademicYear(Document):
	pass
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
