from frappe import _

<<<<<<< HEAD
def get_data():
	return {
		'fieldname': 'supplier_quotation',
		'non_standard_fieldnames': {
			'Subscription': 'reference_document'
		},
		'internal_links': {
			'Material Request': ['items', 'material_request'],
			'Request for Quotation': ['items', 'request_for_quotation'],
			'Project': ['items', 'project'],
		},
		'transactions': [
			{
				'label': _('Related'),
				'items': ['Purchase Order', 'Quotation']
			},
			{
				'label': _('Reference'),
				'items': ['Material Request', 'Request for Quotation', 'Project']
			},
			{
				'label': _('Subscription'),
				'items': ['Subscription']
			},
		]

	}
=======
data = {
	'fieldname': 'supplier_quotation',
	'internal_links': {
		'Material Request': ['items', 'material_request'],
		'Request for Quotation': ['items', 'request_for_quotation'],
		'Project': ['items', 'project'],
	},
	'transactions': [
		{
			'label': _('Related'),
			'items': ['Purchase Order']
		},
		{
			'label': _('Reference'),
			'items': ['Material Request', 'Request for Quotation', 'Project']
		},
	]
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
