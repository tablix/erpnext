# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from frappe.website.website_generator import WebsiteGenerator
<<<<<<< HEAD
=======
from frappe.utils import quoted
from frappe.utils.user import get_fullname_and_avatar
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
from frappe import _

class JobOpening(WebsiteGenerator):
	website = frappe._dict(
		template = "templates/generators/job_opening.html",
		condition_field = "publish",
		page_title_field = "job_title",
	)

<<<<<<< HEAD
	def validate(self):
		if not self.route:
			self.route = frappe.scrub(self.job_title).replace('_', '-')
=======
	def make_route(self):
		return 'jobs/' + self.scrub(self.job_title)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	def get_context(self, context):
		context.parents = [{'name': 'jobs', 'title': _('All Jobs') }]

def get_list_context(context):
	context.title = _("Jobs")
	context.introduction = _('Current Job Openings')
