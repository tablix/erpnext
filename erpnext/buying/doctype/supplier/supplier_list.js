frappe.listview_settings['Supplier'] = {
<<<<<<< HEAD
	add_fields: ["supplier_name", "supplier_type", "image"],
=======
	add_fields: ["supplier_name", "supplier_type", 'status'],
	get_indicator: function(doc) {
		if(doc.status==="Open") {
			return [doc.status, "red", "status,=," + doc.status];
		}
	}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
};
