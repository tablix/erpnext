from frappe import _

<<<<<<< HEAD
def get_data():
	return {
		'heatmap': True,
		'heatmap_message': _('This is based on the attendance of this Student'),
		'fieldname': 'student',
		'transactions': [
			{
				'label': _('Admission'),
				'items': ['Program Enrollment']
			},
			{
				'label': _('Student Activity'),
				'items': ['Student Log', 'Student Group', ]
			},
			{
				'label': _('Assessment'),
				'items': ['Assessment Result']
			},
			{
				'label': _('Attendance'),
				'items': ['Student Attendance', 'Student Leave Application']
			},
			{
				'label': _('Fee'),
				'items': ['Fees']
			}
		]
	}
=======
data = {
	'heatmap': True,
	'heatmap_message': _('This is based on the attendance of this Student'),
	'fieldname': 'student',
	'transactions': [
		{
			'items': ['Student Log', 'Student Group', 'Student Attendance']
		},
		{
			'items': ['Program Enrollment', 'Fees', 'Assessment', 'Guardian']
		}
	]
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
