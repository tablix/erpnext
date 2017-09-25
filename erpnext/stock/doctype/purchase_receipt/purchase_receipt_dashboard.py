from frappe import _

<<<<<<< HEAD
def get_data():
	return {
		'fieldname': 'purchase_receipt_no',
		'non_standard_fieldnames': {
			'Purchase Invoice': 'purchase_receipt',
			'Landed Cost Voucher': 'receipt_document',
			'Subscription': 'reference_document'
		},
		'internal_links': {
			'Purchase Order': ['items', 'purchase_order'],
			'Project': ['items', 'project'],
			'Quality Inspection': ['items', 'quality_inspection'],
		},
		'transactions': [
			{
				'label': _('Related'),
				'items': ['Purchase Invoice', 'Landed Cost Voucher']
			},
			{
				'label': _('Reference'),
				'items': ['Purchase Order', 'Quality Inspection', 'Project']
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
	'fieldname': 'purchase_receipt_no',
	'non_standard_fieldnames': {
		'Purchase Invoice': 'purchase_receipt',
		'Landed Cost Voucher': 'receipt_document'
	},
	'internal_links': {
		'Purchase Order': ['items', 'purchase_order'],
		'Project': ['items', 'project'],
		'Quality Inspection': ['items', 'qa_no'],
	},
	'transactions': [
		{
			'label': _('Related'),
			'items': ['Purchase Invoice', 'Landed Cost Voucher']
		},
		{
			'label': _('Reference'),
			'items': ['Purchase Order', 'Quality Inspection', 'Project']
		},
		{
			'label': _('Returns'),
			'items': ['Stock Entry']
		},
	]
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
