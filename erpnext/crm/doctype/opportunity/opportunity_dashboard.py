from frappe import _

<<<<<<< HEAD
def get_data():
	return {
		'fieldname': 'prevdoc_docname',
		'non_standard_fieldnames': {
			'Supplier Quotation': 'opportunity',
		},
		'transactions': [
			{
				'items': ['Quotation', 'Supplier Quotation']
			},
		]
	}
=======
data = {
	'fieldname': 'opportunity',
	'transactions': [
		{
			'label': _('Related'),
			'items': ['Boq', 'Quotation', 'Sales Order']
		},
	]
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
