from frappe import _

<<<<<<< HEAD
def get_data():
	return {
		'fieldname': 'prevdoc_docname',
		'non_standard_fieldnames': {
			'Subscription': 'reference_document',
		},
		'transactions': [
			{
				'label': _('Sales Order'),
				'items': ['Sales Order']
			},
			{
				'label': _('Subscription'),
				'items': ['Subscription']
			},
		]
	}
=======
data = {
	'fieldname': 'prevdoc_docname',
	'internal_links': {
		'Boq': ['items', 'boq_ref'],
		'Opportunity': ['items', 'opp_ref']
	},
	'transactions': [
		{
			'label': _('Related'),
			'items': ['Sales Order']
		},
		{
			'label': _('Reference'),
			'items': ['Boq', 'Opportunity']
		},
	]
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
