frappe.listview_settings['Customer'] = {
<<<<<<< HEAD
	add_fields: ["customer_name", "territory", "customer_group", "customer_type", "image"],
=======
	add_fields: ["customer_name", "territory", "customer_group", "customer_type", 'status'],
	get_indicator: function(doc) {
		color = {
			'Open': 'red',
			'Active': 'green',
			'Dormant': 'darkgrey'
		}
		return [__(doc.status), color[doc.status], "status,=," + doc.status];
	}

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
};
