# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

<<<<<<< HEAD
from frappe.model.utils.rename_field import update_users_report_view_settings
=======
from frappe.model import update_users_report_view_settings
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
from erpnext.patches.v4_0.fields_to_be_renamed import rename_map

def execute():
	for dt, field_list in rename_map.items():
		for field in field_list:
			update_users_report_view_settings(dt, field[0], field[1])
