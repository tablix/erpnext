frappe.listview_settings['Production Order'] = {
	add_fields: ["bom_no", "status", "sales_order", "qty",
<<<<<<< HEAD
		"produced_qty", "expected_delivery_date", "planned_start_date", "planned_end_date"],
=======
		"produced_qty", "expected_delivery_date"],
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	filters: [["status", "!=", "Stopped"]],
	get_indicator: function(doc) {
		if(doc.status==="Submitted") {
			return [__("Not Started"), "orange", "status,=,Submitted"];
		} else {
			return [__(doc.status), {
				"Draft": "red",
				"Stopped": "red",
				"Not Started": "red",
				"In Process": "orange",
				"Completed": "green",
				"Cancelled": "darkgrey"
			}[doc.status], "status,=," + doc.status];
		}
	}
};
