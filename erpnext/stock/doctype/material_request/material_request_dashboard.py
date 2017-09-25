from frappe import _

<<<<<<< HEAD

def get_data():
	return {
		'fieldname': 'material_request',
		'transactions': [
			{
				'label': _('Related'),
				'items': ['Request for Quotation', 'Supplier Quotation', 'Purchase Order']
			},
			{
				'label': _('Manufacturing'),
				'items': ['Production Order']
			}
		]
	}
=======
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
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
