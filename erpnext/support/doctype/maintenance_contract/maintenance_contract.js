// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

{% include 'erpnext/selling/sales_common.js' %}

frappe.ui.form.on('Maintenance Contract', {
	refresh: function(doc, dt, dn) {

		cur_frm.add_custom_button(__('Sales Order'),
				function() {
					erpnext.utils.map_current_doc({
						method: "erpnext.selling.doctype.sales_order.sales_order.make_preventive_maintenance",
						source_doctype: "Sales Order",
						get_query_filters: {
							so_status: "Approved",
							customer: cur_frm.doc.customer || undefined,
							lead: cur_frm.doc.lead || undefined
						}
						
					})
				}, __("Get items from"), "btn-default");

	
	
	}
});
