from frappe import _

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