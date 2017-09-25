from frappe import _

<<<<<<< HEAD
def get_data():
	return {
		'fieldname': 'purchase_order',
		'non_standard_fieldnames': {
			'Journal Entry': 'reference_name',
			'Payment Entry': 'reference_name',
			'Subscription': 'reference_document'
		},
		'internal_links': {
			'Material Request': ['items', 'material_request'],
			'Supplier Quotation': ['items', 'supplier_quotation'],
			'Project': ['items', 'project'],
		},
		'transactions': [
			{
				'label': _('Related'),
				'items': ['Purchase Receipt', 'Purchase Invoice']
			},
			{
				'label': _('Payment'),
				'items': ['Payment Entry', 'Journal Entry']
			},
			{
				'label': _('Reference'),
				'items': ['Material Request', 'Supplier Quotation', 'Project', 'Subscription']
			},
			{
				'label': _('Sub-contracting'),
				'items': ['Stock Entry']
			},
		]
	}
=======
data = {
	'fieldname': 'purchase_order',
	'internal_links': {
		'Material Request': ['items', 'material_request'],
		'Supplier Quotation': ['items', 'supplier_quotation'],
		'Project': ['project']
	},
	'transactions': [
		{
			'label': _('Related'),
			'items': ['Purchase Receipt', 'Purchase Invoice', 'Journal Entry']
		},
		{
			'label': _('Reference'),
			'items': ['Material Request', 'Supplier Quotation', 'Project']
		},
		{
			'label': _('Sub-contracting'),
			'items': ['Stock Entry']
		},
	]
} 
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
