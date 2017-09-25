from frappe import _

<<<<<<< HEAD
def get_data():
	return {
		'fieldname': 'purchase_invoice',
		'non_standard_fieldnames': {
			'Journal Entry': 'reference_name',
			'Payment Entry': 'reference_name',
			'Payment Request': 'reference_name',
			'Landed Cost Voucher': 'receipt_document',
			'Purchase Invoice': 'return_against',
			'Subscription': 'reference_document'
		},
		'internal_links': {
			'Purchase Order': ['items', 'purchase_order'],
			'Purchase Receipt': ['items', 'purchase_receipt'],
		},
		'transactions': [
			{
				'label': _('Payment'),
				'items': ['Payment Entry', 'Payment Request', 'Journal Entry']
			},
			{
				'label': _('Reference'),
				'items': ['Purchase Order', 'Purchase Receipt', 'Asset', 'Landed Cost Voucher']
			},
			{
				'label': _('Returns'),
				'items': ['Purchase Invoice']
			},
			{
				'label': _('Subscription'),
				'items': ['Subscription']
			},
		]
	}
=======
data = {
	'fieldname': 'purchase_invoice',
	'non_standard_fieldnames': {
		'Delivery Note': 'against_sales_invoice',
		'Journal Entry': 'reference_name',
		'Payment Entry': 'reference_name',
		'Payment Request': 'reference_name',
		'Landed Cost Voucher': 'receipt_document',
		'Purchase Invoice': 'return_against'
	},
	'internal_links': {
		'Purchase Order': ['items', 'sales_order'],
		'Purchase Receipt': ['items', 'delivery_note'],
	},
	'transactions': [
		{
			'label': _('Payment'),
			'items': ['Payment Entry', 'Payment Request', 'Journal Entry']
		},
		{
			'label': _('Reference'),
			'items': ['Purchase Order', 'Purchase Receipt', 'Asset', 'Landed Cost Voucher']
		},
		{
			'label': _('Returns'),
			'items': ['Purchase Invoice']
		},
	]
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
