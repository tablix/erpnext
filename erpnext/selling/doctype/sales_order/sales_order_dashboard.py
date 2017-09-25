from frappe import _

<<<<<<< HEAD
def get_data():
	return {
		'fieldname': 'sales_order',
		'non_standard_fieldnames': {
			'Delivery Note': 'against_sales_order',
			'Journal Entry': 'reference_name',
			'Payment Entry': 'reference_name',
			'Payment Request': 'reference_name',
			'Subscription': 'reference_document',
		},
		'internal_links': {
			'Quotation': ['items', 'prevdoc_docname']
		},
		'transactions': [
			{
				'label': _('Fulfillment'),
				'items': ['Sales Invoice', 'Delivery Note']
			},
			{
				'label': _('Purchasing'),
				'items': ['Material Request', 'Purchase Order']
			},
			{
				'label': _('Projects'),
				'items': ['Project']
			},
			{
				'label': _('Manufacturing'),
				'items': ['Production Order']
			},
			{
				'label': _('Reference'),
				'items': ['Quotation', 'Subscription']
			},
			{
				'label': _('Payment'),
				'items': ['Payment Entry', 'Payment Request', 'Journal Entry']
			},
		]
	}
=======
data = {
	'fieldname': 'sales_order',
	'non_standard_fieldnames': {
		'Delivery Note': 'against_sales_order',
	},
	'internal_links': {
		'Quotation': ['items', 'prevdoc_docname'],
		'Boq': ['items', 'boq_ref'],
		'Opportunity': ['items', 'opp_ref']
	},
	'transactions': [
		{
			'label': _('Fulfillment'),
			'items': ['Sales Invoice', 'Delivery Note']
		},
		{
			'label': _('Purchasing'),
			'items': ['Material Request', 'Purchase Order']
		},
		{
			'label': _('Projects'),
			'items': ['Project']
		},
		{
			'label': _('Manufacturing'),
			'items': ['Production Order']
		},
		{
			'label': _('Reference'),
			'items': ['Opportunity', 'Boq', 'Quotation']
		},
	]
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
