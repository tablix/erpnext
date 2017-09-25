from frappe import _

data = {
	'fieldname': 'material_request',
	'internal_links': {
		'Sales Order': ['items', 'sales_order'],
	},
	'transactions': [
		{
			'label': _('Related'),
			'items': ['Request for Quotation', 'Supplier Quotation', 'Purchase Order']
		},
		{
			'label': _('Reference'),
			'items': ['Sales Order']
		},
	]
}