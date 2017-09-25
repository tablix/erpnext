// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

<<<<<<< HEAD
{% include 'erpnext/public/js/controllers/buying.js' %};

frappe.provide("erpnext.stock");

frappe.ui.form.on("Purchase Receipt", {
	setup: function(frm) {
		frm.custom_make_buttons = {
			'Stock Entry': 'Return',
			'Purchase Invoice': 'Invoice'
		}
	},
	onload: function(frm) {
=======
{% include 'erpnext/buying/doctype/purchase_common/purchase_common.js' %};

frappe.provide("erpnext.stock");


frappe.ui.form.on("Purchase Receipt", {
	setup: function(frm) {
		console.log(frm.get_field('items'));
        frm.get_field('items').grid.editable_fields = [
            {fieldname: 'item_code', columns: 3},
            {fieldname: 'qty', columns: 2},
            {fieldname: 'rate', columns: 2},
            {fieldname: 'amount', columns: 2},
        ];
    },
	
	onload: function(frm) {
		// default values for quotation no
		var qa_no = frappe.meta.get_docfield("Purchase Receipt Item", "qa_no");
		qa_no.get_route_options_for_new_doc = function(field) {
			if(frm.is_new()) return;
			var doc = field.doc;
			return {
				"inspection_type": "Incoming",
				"purchase_receipt_no": frm.doc.name,
				"item_code": doc.item_code,
				"description": doc.description,
				"item_serial_no": doc.serial_no ? doc.serial_no.split("\n")[0] : null,
				"batch_no": doc.batch_no
			}
		}

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		$.each(["warehouse", "rejected_warehouse"], function(i, field) {
			frm.set_query(field, "items", function() {
				return {
					filters: [
						["Warehouse", "company", "in", ["", cstr(frm.doc.company)]],
						["Warehouse", "is_group", "=", 0]
					]
				}
			})
		})

		frm.set_query("supplier_warehouse", function() {
			return {
				filters: [
					["Warehouse", "company", "in", ["", cstr(frm.doc.company)]],
					["Warehouse", "is_group", "=", 0]
				]
			}
<<<<<<< HEAD
		});

	},

	refresh: function(frm) {
		if(frm.doc.company) {
			frm.trigger("toggle_display_account_head");
		}
	},

	company: function(frm) {
		frm.trigger("toggle_display_account_head");
	},

	toggle_display_account_head: function(frm) {
		var enabled = erpnext.is_perpetual_inventory_enabled(frm.doc.company)
		frm.fields_dict["items"].grid.set_column_disp(["cost_center"], enabled);
	},
});

erpnext.stock.PurchaseReceiptController = erpnext.buying.BuyingController.extend({
	setup: function(doc) {
		this.setup_posting_date_time_check();
		this._super(doc);
	},

	refresh: function() {
		var me = this;
		this._super();
		if(this.frm.doc.docstatus===1) {
			this.show_stock_ledger();
			if (erpnext.is_perpetual_inventory_enabled(this.frm.doc.company)) {
=======
		})
	}
	
});

erpnext.stock.PurchaseReceiptController = erpnext.buying.BuyingController.extend({
	refresh: function() {
		this._super();
		if(this.frm.doc.docstatus===1) {
			this.show_stock_ledger();
			if (cint(frappe.defaults.get_default("auto_accounting_for_stock"))) {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				this.show_general_ledger();
			}
		}

		if(!this.frm.doc.is_return && this.frm.doc.status!="Closed") {
<<<<<<< HEAD
			if (this.frm.doc.docstatus == 0) {
				this.frm.add_custom_button(__('Purchase Order'),
					function () {
						erpnext.utils.map_current_doc({
							method: "erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_receipt",
							source_doctype: "Purchase Order",
							target: me.frm,
							setters: {
								supplier: me.frm.doc.supplier || undefined,
							},
							get_query_filters: {
								docstatus: 1,
								status: ["!=", "Closed"],
								per_received: ["<", 99.99],
								company: me.frm.doc.company
							}
						})
					}, __("Get items from"));
=======
			if(this.frm.doc.docstatus==0) {
				cur_frm.add_custom_button(__('Purchase Order'),
					function() {
						erpnext.utils.map_current_doc({
							method: "erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_receipt",
							source_doctype: "Purchase Order",
							get_query_filters: {
								supplier: cur_frm.doc.supplier || undefined,
								docstatus: 1,
								status: ["!=", "Closed"],
								per_received: ["<", 99.99],
								company: cur_frm.doc.company
							}
						})
				}, __("Get items from"));
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			}

			if(this.frm.doc.docstatus == 1 && this.frm.doc.status!="Closed") {
				if (this.frm.has_perm("submit")) {
					cur_frm.add_custom_button(__("Close"), this.close_purchase_receipt, __("Status"))
				}

				cur_frm.add_custom_button(__('Return'), this.make_purchase_return, __("Make"));
<<<<<<< HEAD
=======
				
				cur_frm.add_custom_button(__('Delivery Note'), this.make_delivery_note, __("Make"));
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

				if(flt(this.frm.doc.per_billed) < 100) {
					cur_frm.add_custom_button(__('Invoice'), this.make_purchase_invoice, __("Make"));
				}
<<<<<<< HEAD

				if(!this.frm.doc.subscription) {
					cur_frm.add_custom_button(__('Subscription'), function() {
						erpnext.utils.make_subscription(me.frm.doc.doctype, me.frm.doc.name)
					}, __("Make"))
				}

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
			}
		}


		if(this.frm.doc.docstatus==1 && this.frm.doc.status === "Closed" && this.frm.has_perm("submit")) {
			cur_frm.add_custom_button(__('Reopen'), this.reopen_purchase_receipt, __("Status"))
		}

		this.frm.toggle_reqd("supplier_warehouse", this.frm.doc.is_subcontracted==="Yes");
<<<<<<< HEAD
=======
		
		//new addition
		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	},

	make_purchase_invoice: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_purchase_invoice",
			frm: cur_frm
		})
	},

	make_purchase_return: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_purchase_return",
			frm: cur_frm
		})
	},
<<<<<<< HEAD

=======
	
	make_delivery_note: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_delivery_note",
			frm: cur_frm
		})
	},
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	close_purchase_receipt: function() {
		cur_frm.cscript.update_status("Closed");
	},

	reopen_purchase_receipt: function() {
		cur_frm.cscript.update_status("Submitted");
	}

});

// for backward compatibility: combine new and previous states
$.extend(cur_frm.cscript, new erpnext.stock.PurchaseReceiptController({frm: cur_frm}));

cur_frm.cscript.update_status = function(status) {
	frappe.ui.form.is_saving = true;
	frappe.call({
		method:"erpnext.stock.doctype.purchase_receipt.purchase_receipt.update_purchase_receipt_status",
		args: {docname: cur_frm.doc.name, status: status},
		callback: function(r){
			if(!r.exc)
				cur_frm.reload_doc();
		},
		always: function(){
			frappe.ui.form.is_saving = false;
		}
	})
}

<<<<<<< HEAD
=======
cur_frm.fields_dict['supplier_address'].get_query = function(doc, cdt, cdn) {
	return {
		filters: { 'supplier': doc.supplier}
	}
}

cur_frm.fields_dict['contact_person'].get_query = function(doc, cdt, cdn) {
	return {
		filters: { 'supplier': doc.supplier }
	}
}

cur_frm.cscript.new_contact = function() {
	tn = frappe.model.make_new_doc_and_get_name('Contact');
	locals['Contact'][tn].is_supplier = 1;
	if(doc.supplier)
		locals['Contact'][tn].supplier = doc.supplier;
	frappe.set_route('Form', 'Contact', tn);
}

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
cur_frm.fields_dict['items'].grid.get_field('project').get_query = function(doc, cdt, cdn) {
	return {
		filters: [
			['Project', 'status', 'not in', 'Completed, Cancelled']
		]
	}
}

<<<<<<< HEAD
=======
cur_frm.fields_dict['items'].grid.get_field('batch_no').get_query= function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	if(d.item_code) {
		return {
			filters: {'item': d.item_code}
		}
	}
	else
		msgprint(__("Please enter Item Code."));
}

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
cur_frm.cscript.select_print_heading = function(doc, cdt, cdn) {
	if(doc.select_print_heading)
		cur_frm.pformat.print_heading = doc.select_print_heading;
	else
		cur_frm.pformat.print_heading = "Purchase Receipt";
}

cur_frm.fields_dict['select_print_heading'].get_query = function(doc, cdt, cdn) {
	return {
		filters: [
			['Print Heading', 'docstatus', '!=', '2']
		]
	}
}

<<<<<<< HEAD
=======
cur_frm.fields_dict.items.grid.get_field("qa_no").get_query = function(doc) {
	return {
		filters: {
			'docstatus': 1
		}
	}
}

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
cur_frm.fields_dict['items'].grid.get_field('bom').get_query = function(doc, cdt, cdn) {
	var d = locals[cdt][cdn]
	return {
		filters: [
			['BOM', 'item', '=', d.item_code],
			['BOM', 'is_active', '=', '1'],
			['BOM', 'docstatus', '=', '1']
		]
	}
}

cur_frm.cscript.on_submit = function(doc, cdt, cdn) {
	if(cint(frappe.boot.notification_settings.purchase_receipt))
		cur_frm.email_doc(frappe.boot.notification_settings.purchase_receipt_message);
}

frappe.provide("erpnext.buying");

frappe.ui.form.on("Purchase Receipt", "is_subcontracted", function(frm) {
	if (frm.doc.is_subcontracted === "Yes") {
		erpnext.buying.get_default_bom(frm);
	}
	frm.toggle_reqd("supplier_warehouse", frm.doc.is_subcontracted==="Yes");
});
