from frappe import _

<<<<<<< HEAD
def get_data():
	return {
		'docstatus': 1,
		'fieldname': 'request_for_quotation',
		'transactions': [
			{
				'items': ['Supplier Quotation']
			},
		]
	}
=======
data = {
	'docstatus': 1,
	'fieldname': 'request_for_quotation',
	'transactions': [
		{
			'label': _('Related'),
			'items': ['Supplier Quotation']
		},
	]
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
