from frappe import _

<<<<<<< HEAD
def get_data():
	return {
		'fieldname': 'sales_invoice',
		'non_standard_fieldnames': {
			'Delivery Note': 'against_sales_invoice',
			'Journal Entry': 'reference_name',
			'Payment Entry': 'reference_name',
			'Payment Request': 'reference_name',
			'Sales Invoice': 'return_against',
			'Subscription': 'reference_document',
		},
		'internal_links': {
			'Sales Order': ['items', 'sales_order']
		},
		'transactions': [
			{
				'label': _('Payment'),
				'items': ['Payment Entry', 'Payment Request', 'Journal Entry']
			},
			{
				'label': _('Reference'),
				'items': ['Timesheet', 'Delivery Note', 'Sales Order']
			},
			{
				'label': _('Returns'),
				'items': ['Sales Invoice']
			},
			{
				'label': _('Subscription'),
				'items': ['Subscription']
			},
		]
	}
=======
data = {
	'fieldname': 'sales_invoice',
	'non_standard_fieldnames': {
		'Delivery Note': 'against_sales_invoice',
		'Journal Entry': 'reference_name',
		'Payment Entry': 'reference_name',
		'Payment Request': 'reference_name',
		'Sales Invoice': 'return_against'
	},
	'internal_links': {
		'Sales Order': ['items', 'sales_order'],
		'Delivery Note': ['items', 'delivery_note'],
	},
	'transactions': [
		{
			'label': _('Payment'),
			'items': ['Payment Entry', 'Payment Request', 'Journal Entry']
		},
		{
			'label': _('Reference'),
			'items': ['Timesheet', 'Delivery Note', 'Sales Order']
		},
		{
			'label': _('Returns'),
			'items': ['Sales Invoice']
		},
	]
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
