from frappe import _

<<<<<<< HEAD
def get_data():
	return {
		'fieldname': 'delivery_note',
		'non_standard_fieldnames': {
			'Stock Entry': 'delivery_note_no',
			'Quality Inspection': 'reference_name',
			'Subscription': 'reference_document',
		},
		'internal_links': {
			'Sales Order': ['items', 'against_sales_order'],
		},
		'transactions': [
			{
				'label': _('Related'),
				'items': ['Sales Invoice', 'Packing Slip']
			},
			{
				'label': _('Reference'),
				'items': ['Sales Order', 'Quality Inspection']
			},
			{
				'label': _('Returns'),
				'items': ['Stock Entry']
			},
			{
				'label': _('Subscription'),
				'items': ['Subscription']
			},
		]
	}
=======
data = {
	'fieldname': 'delivery_note_no',
	'non_standard_fieldnames': {
		'Sales Invoice': 'delivery_note',
		'Packing Slip': 'delivery_note',
	},
	'internal_links': {
		'Sales Order': ['items', 'against_sales_order'],
	},
	'transactions': [
		{
			'label': _('Related'),
			'items': ['Sales Invoice', 'Packing Slip']
		},
		{
			'label': _('Reference'),
			'items': ['Sales Order', 'Quality Inspection']
		},
		{
			'label': _('Returns'),
			'items': ['Stock Entry']
		},
	]
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
