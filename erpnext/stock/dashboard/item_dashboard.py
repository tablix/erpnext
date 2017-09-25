from __future__ import unicode_literals

import frappe

@frappe.whitelist()
<<<<<<< HEAD
def get_data(item_code=None, warehouse=None, item_group=None,
	start=0, sort_by='actual_qty', sort_order='desc'):
	'''Return data to render the item dashboard'''
	conditions = []
	values = []
	if item_code:
		conditions.append('b.item_code=%s')
		values.append(item_code)
	if warehouse:
		conditions.append('b.warehouse=%s')
		values.append(warehouse)
	if item_group:
		conditions.append('i.item_group=%s')
		values.append(item_group)

	if conditions:
		conditions = ' and ' + ' and '.join(conditions)
	else:
		conditions = ''

	return frappe.db.sql('''
	select
		b.item_code, b.warehouse, b.projected_qty, b.reserved_qty,
		b.reserved_qty_for_production, b.actual_qty, b.valuation_rate, i.item_name
	from
		tabBin b, tabItem i
	where
		b.item_code = i.name
		and
		(b.projected_qty != 0 or b.reserved_qty != 0 or b.reserved_qty_for_production != 0 or b.actual_qty != 0)
		{conditions}
	order by
		{sort_by} {sort_order}
	limit
		{start}, 21
	'''.format(conditions=conditions, sort_by=sort_by, sort_order=sort_order,
		start=start), values, as_dict=True)
=======
def get_data(item_code=None, warehouse=None, start=0, sort_by='actual_qty', sort_order='desc'):
	filters = {}
	if item_code:
		filters['item_code'] = item_code
	if warehouse:
		filters['warehouse'] = warehouse
	return frappe.get_list("Bin", filters=filters, fields=['item_code', 'warehouse',
		'projected_qty', 'reserved_qty', 'reserved_qty_for_production', 'actual_qty', 'valuation_rate'],
		order_by='{0} {1}'.format(sort_by, sort_order), start=start, page_length = 21)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
