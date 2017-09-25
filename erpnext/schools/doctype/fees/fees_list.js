frappe.listview_settings['Fees'] = {
<<<<<<< HEAD
	add_fields: ["grand_total", "outstanding_amount", "due_date"],
	get_indicator: function(doc) {
		if(flt(doc.outstanding_amount)==0) {
			return [__("Paid"), "green", "outstanding_amount,=,0"];
		} else if (flt(doc.outstanding_amount) > 0 && doc.due_date >= frappe.datetime.get_today()) {
			return [__("Unpaid"), "orange", "outstanding_amount,>,0|due_date,>,Today"];
		} else if (flt(doc.outstanding_amount) > 0 && doc.due_date < frappe.datetime.get_today()) {
			return [__("Overdue"), "red", "outstanding_amount,>,0|due_date,<=,Today"];
=======
	add_fields: [ "total_amount", "paid_amount", "due_date"],
	get_indicator: function(doc) {
		if ((doc.total_amount > doc.paid_amount) && doc.due_date < get_today()) {
			return [__("Overdue"), "red", ["due_date,<,"+get_today()], ["due_date,<,"+get_today()]];
		}
		else if (doc.total_amount > doc.paid_amount) {
			return [__("Pending"), "orange"];
		}
		else {
			return [__("Paid"), "green"];
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		}
	}
};