frappe.listview_settings['Expense Claim'] = {
	add_fields: ["approval_status", "total_claimed_amount", "docstatus"],
	filters:[["approval_status","!=", "Rejected"]],
	get_indicator: function(doc) {
<<<<<<< HEAD
		if(doc.status == "Paid") {
			return [__("Paid"), "green", "status,=,'Paid'"];
		}else if(doc.status == "Unpaid") {
			return [__("Unpaid"), "orange"];
		} else if(doc.status == "Rejected") {
			return [__("Rejected"), "grey"];
		}
=======
		return [__(doc.approval_status), frappe.utils.guess_colour(doc.approval_status),
			"approval_status,=," + doc.approval_status];
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	}
};
