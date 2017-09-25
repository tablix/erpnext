from frappe import _

<<<<<<< HEAD
def get_data():
	return {
		'heatmap': True,
		'heatmap_message': _('This is based on the attendance of this Employee'),
		'fieldname': 'employee',
		'transactions': [
			{
				'label': _('Leave and Attendance'),
				'items': ['Attendance', 'Leave Application', 'Leave Allocation']
			},
			{
				'label': _('Payroll'),
				'items': ['Salary Structure', 'Salary Slip', 'Timesheet']
			},
			{
				'label': _('Training Events/Results'),
				'items': ['Training Event', 'Training Result']
			},
			{
				'label': _('Expense'),
				'items': ['Expense Claim']
			},
			{
				'label': _('Evaluation'),
				'items': ['Appraisal']
			}
		]
	}
=======
data = {
	'heatmap': True,
	'heatmap_message': _('This is based on the attendance of this Employee'),
	'fieldname': 'employee',
	'transactions': [
		{
			'label': _('Leave and Attendance'),
			'items': ['Attendance', 'Leave Application', 'Leave Allocation']
		},
		{
			'label': _('Payroll'),
			'items': ['Salary Structure', 'Salary Slip', 'Timesheet']
		},
		{
			'label': _('Expense'),
			'items': ['Expense Claim']
		},
		{
			'label': _('Evaluation'),
			'items': ['Appraisal']
		}
	]
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
