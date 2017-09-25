from frappe import _

<<<<<<< HEAD
def get_data():
	return {
		'heatmap': True,
		'heatmap_message': _('This is based on transactions against this Customer. See timeline below for details'),
		'fieldname': 'customer',
		'transactions': [
			{
				'label': _('Pre Sales'),
				'items': ['Opportunity', 'Quotation']
			},
			{
				'label': _('Orders'),
				'items': ['Sales Order', 'Delivery Note', 'Sales Invoice']
			},
			{
				'label': _('Support'),
				'items': ['Issue']
			},
			{
				'label': _('Projects'),
				'items': ['Project']
			}
		]
	}
=======
data = {
	'heatmap': True,
	'heatmap_message': _('This is based on transactions against this Customer. See timeline below for details'),
	'fieldname': 'customer',
	'transactions': [
		{
			'label': _('Pre Sales'),
			'items': ['Opportunity', 'Quotation']
		},
		{
			'label': _('Orders'),
			'items': ['Sales Order', 'Delivery Note', 'Sales Invoice']
		},
		{
			'label': _('Support'),
			'items': ['Issue']
		},
		{
			'label': _('Projects'),
			'items': ['Project']
		}
	]
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
