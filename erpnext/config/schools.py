from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Student"),
			"items": [
<<<<<<< HEAD
=======

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				{
					"type": "doctype",
					"name": "Student"
				},
				{
					"type": "doctype",
<<<<<<< HEAD
					"name": "Guardian"
				},
				{
					"type": "doctype",
					"name": "Student Log"
=======
					"name": "Student Log"
				},
				{
					"type": "doctype",
					"name": "Student Batch"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				},
				{
					"type": "doctype",
					"name": "Student Group"
				},
				{
					"type": "doctype",
					"name": "Student Group Creation Tool"
<<<<<<< HEAD
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Student and Guardian Contact Details",
					"doctype": "Program Enrollment"
				}

=======
				}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			]
		},
		{
			"label": _("Admission"),
			"items": [

				{
					"type": "doctype",
					"name": "Student Applicant"
				},
				{
					"type": "doctype",
<<<<<<< HEAD
					"name": "Student Admission"
				},
				{
					"type": "doctype",
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
					"name": "Program Enrollment"
				},
				{
					"type": "doctype",
					"name": "Program Enrollment Tool"
				}
			]
		},
		{
<<<<<<< HEAD
			"label": _("Attendance"),
			"items": [
				{
					"type": "doctype",
					"name": "Student Attendance"
				},
				{
					"type": "doctype",
					"name": "Student Leave Application"
				},
				{
					"type": "doctype",
					"name": "Student Attendance Tool"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Absent Student Report",
					"doctype": "Student Attendance"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Student Batch-Wise Attendance",
					"doctype": "Student Attendance"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Student Monthly Attendance Sheet",
					"doctype": "Student Attendance"
				}
			]
		},
		{
			"label": _("Schedule"),
			"items": [
				{
					"type": "doctype",
					"name": "Course Schedule",
					"route": "List/Course Schedule/Calendar"
				},
				{
					"type": "doctype",
					"name": "Course Scheduling Tool"
=======
			"label": _("Schedule"),
			"items": [
				{
					"type": "doctype",
					"name": "Course Schedule",
					"route": "Calendar/Course Schedule"
				},
				{
					"type": "doctype",
					"name": "Student Attendance"
				},
				{
					"type": "doctype",
					"name": "Assessment"
				},
				{
					"type": "doctype",
					"name": "Assessment Group"
				},
				{
					"type": "doctype",
					"name": "Scheduling Tool"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				}
			]
		},
		{
<<<<<<< HEAD
			"label": _("Assessment"),
			"items": [
				{
					"type": "doctype",
					"name": "Assessment Plan"
				},
				{
					"type": "doctype",
					"name": "Assessment Group",
					"link": "Tree/Assessment Group",
				},
				{
					"type": "doctype",
					"name": "Assessment Result"
				},
				{
					"type": "doctype",
					"name": "Grading Scale"
				},
				{
					"type": "doctype",
					"name": "Assessment Criteria"
				},
				{
					"type": "doctype",
					"name": "Assessment Criteria Group"
				},
				{
					"type": "doctype",
					"name": "Assessment Result Tool"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Course wise Assessment Report",
					"doctype": "Assessment Result"
				},

			]
		},
		{
			"label": _("Fees"),
			"items": [
				{
					"type": "doctype",
					"name": "Fees"
				},
				{
					"type": "doctype",
					"name": "Fee Schedule"
				},
				{
					"type": "doctype",
					"name": "Fee Structure"
				},
				{
					"type": "doctype",
					"name": "Fee Category"
				},
				{
					"type": "report",
					"name": "Student Fee Collection",
					"doctype": "Fees",
					"is_query_report": True
=======
			"label": _("Fees"),
			"items": [
				{
					"type": "doctype",
					"name": "Fees"
				},
				{
					"type": "doctype",
					"name": "Fee Structure"
				},
				{
					"type": "doctype",
					"name": "Fee Category"
				},
				{
					"type": "report",
					"name": "Student Fee Collection",
					"doctype": "Fees",
					"is_query_report": True
				}
			]
		},
		{
			"label": _("LMS"),
			"items": [
				{
					"type": "doctype",
					"name": "Announcement"
				},
				{
					"type": "doctype",
					"name": "Topic"
				},
				{
					"type": "doctype",
					"name": "Discussion"
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				}
			]
		},
		{
			"label": _("Setup"),
			"items": [
				{
					"type": "doctype",
					"name": "Course"
				},
				{
					"type": "doctype",
					"name": "Program"
				},
				{
					"type": "doctype",
					"name": "Instructor"
				},
				{
					"type": "doctype",
					"name": "Room"
				},
				{
					"type": "doctype",
<<<<<<< HEAD
					"name": "Student Category"
				},
				{
					"type": "doctype",
					"name": "Student Batch Name"
				},
				{
					"type": "doctype",
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
					"name": "Academic Term"
				},
				{
					"type": "doctype",
					"name": "Academic Year"
<<<<<<< HEAD
				},
				{
					"type": "doctype",
					"name": "School Settings"
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				}
			]
		},
	]
