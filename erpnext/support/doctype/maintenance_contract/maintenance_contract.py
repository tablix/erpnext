# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

import datetime
from calendar import monthrange
from frappe.utils import getdate, validate_email_add, today, add_years , add_months

class MaintenanceContract(Document):
	pass
	def validate(self):
		self.update_schdl_table()
	
	
	def update_schdl_table(self):
		i=0
		j = 0
		for dt in self.get("scheduling") :
			j = j +1
		if j == 1:
			for dt in self.get("scheduling") :
				st_date = dt.start_date 
				end_date = dt.end_date
				break
			if self.contract_start_date is not None and self.contract_end_date is not None and dt.start_date is not None and dt.end_date is not None:
				if self.amc_duration == "Monthly" :
					if self.contract_start_date <= st_date and self.contract_end_date >= end_date :
						if end_date >= st_date :
							schdl_st_date = datetime.datetime.strptime(st_date,"%Y-%m-%d")
							schdl_end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
							contract_end_date1 = datetime.datetime.strptime(self.contract_end_date ,"%Y-%m-%d")
							while i >= 0 :
								schdl_st_date= add_months(schdl_st_date , 1)
								schdl_end_date= add_months(schdl_end_date , 1)
								if schdl_end_date > contract_end_date1 or schdl_st_date >=contract_end_date1:
									break
								else:
									self.append("scheduling", {"start_date":schdl_st_date.strftime("%Y-%m-%d") , "end_date":schdl_end_date.strftime("%Y-%m-%d")})
				
				if self.amc_duration == "Quarterly" :
					if self.contract_start_date <= st_date and self.contract_end_date >= end_date :
						if end_date >= st_date :
							schdl_st_date = datetime.datetime.strptime(st_date,"%Y-%m-%d")
							schdl_end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
							contract_end_date1 = datetime.datetime.strptime(self.contract_end_date ,"%Y-%m-%d")
							while i >= 0 :
								schdl_st_date= add_months(schdl_st_date , 3)
								schdl_end_date= add_months(schdl_end_date , 3)
								if schdl_end_date > contract_end_date1 or schdl_st_date >=contract_end_date1:
									break
								else:
									self.append("scheduling", {"start_date":schdl_st_date.strftime("%Y-%m-%d") , "end_date":schdl_end_date.strftime("%Y-%m-%d")})
				
				if self.amc_duration == "Yearly" :
					if self.contract_start_date <= st_date and self.contract_end_date >= end_date :
						if end_date >= st_date :
							schdl_st_date = datetime.datetime.strptime(st_date,"%Y-%m-%d")
							schdl_end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
							contract_end_date1 = datetime.datetime.strptime(self.contract_end_date ,"%Y-%m-%d")
							while i >= 0 :
								schdl_st_date= add_years(schdl_st_date , 1)
								schdl_end_date= add_years(schdl_end_date , 1)
								if schdl_end_date > contract_end_date1 or schdl_st_date >=contract_end_date1:
									break
								else:
									self.append("scheduling", {"start_date":schdl_st_date.strftime("%Y-%m-%d"), "end_date":schdl_end_date.strftime("%Y-%m-%d")})
				
			else:
				frappe.msgprint("No")
