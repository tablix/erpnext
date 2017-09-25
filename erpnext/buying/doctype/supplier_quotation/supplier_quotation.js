// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// attach required files
<<<<<<< HEAD
{% include 'erpnext/public/js/controllers/buying.js' %};

frappe.ui.form.on('Suppier Quotation', {
	setup: function(frm) {
		frm.custom_make_buttons = {
			'Purchase Order': 'Purchase Order'
		}
	}
});

erpnext.buying.SupplierQuotationController = erpnext.buying.BuyingController.extend({
	refresh: function() {
		var me = this;
=======
{% include 'erpnext/buying/doctype/purchase_common/purchase_common.js' %};

erpnext.buying.SupplierQuotationController = erpnext.buying.BuyingController.extend({
	refresh: function() {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		this._super();
		if (this.frm.doc.docstatus === 1) {
			cur_frm.add_custom_button(__("Purchase Order"), this.make_purchase_order,
				__("Make"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
<<<<<<< HEAD
			cur_frm.add_custom_button(__("Quotation"), this.make_quotation,
				__("Make"));
			cur_frm.add_custom_button(__('Subscription'), function() {
				erpnext.utils.make_subscription(me.frm.doc.doctype, me.frm.doc.name)
			}, __("Make"))
		}
		else if (this.frm.doc.docstatus===0) {

			this.frm.add_custom_button(__('Material Request'),
=======
		}
		else if (this.frm.doc.docstatus===0) {
			cur_frm.add_custom_button(__('Material Request'),
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				function() {
					erpnext.utils.map_current_doc({
						method: "erpnext.stock.doctype.material_request.material_request.make_supplier_quotation",
						source_doctype: "Material Request",
<<<<<<< HEAD
						target: me.frm,
						setters: {
							company: me.frm.doc.company
						},
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
						get_query_filters: {
							material_request_type: "Purchase",
							docstatus: 1,
							status: ["!=", "Stopped"],
<<<<<<< HEAD
							per_ordered: ["<", 99.99]
=======
							per_ordered: ["<", 99.99],
							company: cur_frm.doc.company
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
						}
					})
				}, __("Get items from"));
		}
	},

	make_purchase_order: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.buying.doctype.supplier_quotation.supplier_quotation.make_purchase_order",
			frm: cur_frm
		})
<<<<<<< HEAD
	},
	make_quotation: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.buying.doctype.supplier_quotation.supplier_quotation.make_quotation",
			frm: cur_frm
		})

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	}
});

// for backward compatibility: combine new and previous states
$.extend(cur_frm.cscript, new erpnext.buying.SupplierQuotationController({frm: cur_frm}));

<<<<<<< HEAD
=======
cur_frm.cscript.uom = function(doc, cdt, cdn) {
	// no need to trigger updation of stock uom, as this field doesn't exist in supplier quotation
}

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
cur_frm.fields_dict['items'].grid.get_field('project').get_query =
	function(doc, cdt, cdn) {
		return{
			filters:[
				['Project', 'status', 'not in', 'Completed, Cancelled']
			]
		}
	}
<<<<<<< HEAD
=======

cur_frm.fields_dict['supplier_address'].get_query = function(doc, cdt, cdn) {
	return {
		filters:{'supplier': doc.supplier}
	}
}

cur_frm.fields_dict['contact_person'].get_query = function(doc, cdt, cdn) {
	return {
		filters:{'supplier': doc.supplier}
	}
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
