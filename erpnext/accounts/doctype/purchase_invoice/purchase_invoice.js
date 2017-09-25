// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.accounts");
<<<<<<< HEAD
{% include 'erpnext/public/js/controllers/buying.js' %};

erpnext.accounts.PurchaseInvoice = erpnext.buying.BuyingController.extend({
	setup: function(doc) {
		this.setup_posting_date_time_check();
		this._super(doc);
	},
=======
{% include 'erpnext/buying/doctype/purchase_common/purchase_common.js' %};


erpnext.accounts.PurchaseInvoice = erpnext.buying.BuyingController.extend({
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	onload: function() {
		this._super();

		if(!this.frm.doc.__islocal) {
			// show credit_to in print format
			if(!this.frm.doc.supplier && this.frm.doc.credit_to) {
				this.frm.set_df_property("credit_to", "print_hide", 0);
			}
		}

		// formatter for material request item
		this.frm.set_indicator_formatter('item_code',
			function(doc) { return (doc.qty<=doc.received_qty) ? "green" : "orange" })

	},

	refresh: function(doc) {
		this._super();

		hide_fields(this.frm.doc);
		// Show / Hide button
		this.show_general_ledger();

		if(doc.update_stock==1 && doc.docstatus==1) {
			this.show_stock_ledger();
		}

		if(!doc.is_return && doc.docstatus==1) {
			if(doc.outstanding_amount != 0) {
				this.frm.add_custom_button(__('Payment'), this.make_payment_entry, __("Make"));
				cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
			}

			if(doc.outstanding_amount >= 0 || Math.abs(flt(doc.outstanding_amount)) < flt(doc.grand_total)) {
<<<<<<< HEAD
				cur_frm.add_custom_button(__('Return / Debit Note'),
					this.make_debit_note, __("Make"));
			}

			if(!doc.subscription) {
				cur_frm.add_custom_button(__('Subscription'), function() {
					erpnext.utils.make_subscription(doc.doctype, doc.name)
				}, __("Make"))
			}
		}

		if(doc.docstatus===0) {
			var me = this;
			this.frm.add_custom_button(__('Purchase Order'), function() {
				erpnext.utils.map_current_doc({
					method: "erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_invoice",
					source_doctype: "Purchase Order",
					target: me.frm,
					setters: {
						supplier: me.frm.doc.supplier || undefined,
					},
					get_query_filters: {
						docstatus: 1,
						status: ["!=", "Closed"],
						per_billed: ["<", 99.99],
						company: me.frm.doc.company
=======
				cur_frm.add_custom_button(doc.update_stock ? __('Purchase Return') : __('Debit Note'),
					this.make_debit_note, __("Make"));
			}
		}

		if(doc.docstatus===0) {
			cur_frm.add_custom_button(__('Purchase Order'), function() {
				erpnext.utils.map_current_doc({
					method: "erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_invoice",
					source_doctype: "Purchase Order",
					get_query_filters: {
						supplier: cur_frm.doc.supplier || undefined,
						docstatus: 1,
						status: ["!=", "Closed"],
						per_billed: ["<", 99.99],
						company: cur_frm.doc.company
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
					}
				})
			}, __("Get items from"));

<<<<<<< HEAD
			this.frm.add_custom_button(__('Purchase Receipt'), function() {
				erpnext.utils.map_current_doc({
					method: "erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_purchase_invoice",
					source_doctype: "Purchase Receipt",
					target: me.frm,
					date_field: "posting_date",
					setters: {
						supplier: me.frm.doc.supplier || undefined,
					},
					get_query_filters: {
						docstatus: 1,
						status: ["not in", ["Closed", "Completed"]],
						company: me.frm.doc.company,
						is_return: 0
=======
			cur_frm.add_custom_button(__('Purchase Receipt'), function() {
				erpnext.utils.map_current_doc({
					method: "erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_purchase_invoice",
					source_doctype: "Purchase Receipt",
					get_query_filters: {
						supplier: cur_frm.doc.supplier || undefined,
						docstatus: 1,
						status: ["!=", "Closed"],
						company: cur_frm.doc.company
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
					}
				})
			}, __("Get items from"));
		}

		this.frm.toggle_reqd("supplier_warehouse", this.frm.doc.is_subcontracted==="Yes");
	},

	supplier: function() {
		var me = this;
		if(this.frm.updating_party_details)
			return;
		erpnext.utils.get_party_details(this.frm, "erpnext.accounts.party.get_party_details",
			{
				posting_date: this.frm.doc.posting_date,
				party: this.frm.doc.supplier,
				party_type: "Supplier",
				account: this.frm.doc.credit_to,
				price_list: this.frm.doc.buying_price_list,
			}, function() {
<<<<<<< HEAD
				me.apply_pricing_rule();
			})
=======
			me.apply_pricing_rule();
		})
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	},

	credit_to: function() {
		var me = this;
		if(this.frm.doc.credit_to) {
			me.frm.call({
				method: "frappe.client.get_value",
				args: {
					doctype: "Account",
					fieldname: "account_currency",
					filters: { name: me.frm.doc.credit_to },
				},
				callback: function(r, rt) {
					if(r.message) {
						me.frm.set_value("party_account_currency", r.message.account_currency);
						me.set_dynamic_labels();
					}
				}
			});
		}
	},

	is_paid: function() {
		hide_fields(this.frm.doc);
		if(cint(this.frm.doc.is_paid)) {
			if(!this.frm.doc.company) {
<<<<<<< HEAD
				this.frm.set_value("is_paid", 0)
				frappe.msgprint(__("Please specify Company to proceed"));
=======
				cur_frm.set_value("is_paid", 0)
				msgprint(__("Please specify Company to proceed"));
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			}
		}
		this.calculate_outstanding_amount();
		this.frm.refresh_fields();
	},

	write_off_amount: function() {
		this.set_in_company_currency(this.frm.doc, ["write_off_amount"]);
		this.calculate_outstanding_amount();
		this.frm.refresh_fields();
	},

	paid_amount: function() {
		this.set_in_company_currency(this.frm.doc, ["paid_amount"]);
		this.write_off_amount();
		this.frm.refresh_fields();
	},

	allocated_amount: function() {
		this.calculate_total_advance();
		this.frm.refresh_fields();
	},

	items_add: function(doc, cdt, cdn) {
		var row = frappe.get_doc(cdt, cdn);
		this.frm.script_manager.copy_from_first_row("items", row,
			["expense_account", "cost_center", "project"]);
	},

	on_submit: function() {
		$.each(this.frm.doc["items"] || [], function(i, row) {
			if(row.purchase_receipt) frappe.model.clear_doc("Purchase Receipt", row.purchase_receipt)
		})
	},

	make_debit_note: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.accounts.doctype.purchase_invoice.purchase_invoice.make_debit_note",
			frm: cur_frm
		})
	},

	asset: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if(row.asset) {
			frappe.call({
				method: "erpnext.accounts.doctype.purchase_invoice.purchase_invoice.get_fixed_asset_account",
				args: {
					"asset": row.asset,
					"account": row.expense_account
				},
				callback: function(r, rt) {
					frappe.model.set_value(cdt, cdn, "expense_account", r.message);
				}
			})
		}
	}
});

cur_frm.script_manager.make(erpnext.accounts.PurchaseInvoice);

// Hide Fields
// ------------
function hide_fields(doc) {
<<<<<<< HEAD
	var parent_fields = ['due_date', 'is_opening', 'advances_section', 'from_date', 'to_date'];
=======
	parent_fields = ['due_date', 'is_opening', 'advances_section', 'from_date', 'to_date'];
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	if(cint(doc.is_paid) == 1) {
		hide_field(parent_fields);
	} else {
<<<<<<< HEAD
		for (var i in parent_fields) {
=======
		for (i in parent_fields) {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			var docfield = frappe.meta.docfield_map[doc.doctype][parent_fields[i]];
			if(!docfield.hidden) unhide_field(parent_fields[i]);
		}

	}

<<<<<<< HEAD
	var item_fields_stock = ['warehouse_section', 'received_qty', 'rejected_qty'];

	cur_frm.fields_dict['items'].grid.set_column_disp(item_fields_stock,
		(cint(doc.update_stock)==1 || cint(doc.is_return)==1 ? true : false));
=======
	item_fields_stock = ['warehouse_section', 'received_qty', 'rejected_qty'];

	cur_frm.fields_dict['items'].grid.set_column_disp(item_fields_stock,
		(cint(doc.update_stock)==1 ? true : false));
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

	cur_frm.refresh_fields();
}

cur_frm.cscript.update_stock = function(doc, dt, dn) {
	hide_fields(doc, dt, dn);
<<<<<<< HEAD
	this.frm.fields_dict.items.grid.toggle_reqd("item_code", doc.update_stock? true: false)
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
}

cur_frm.fields_dict.cash_bank_account.get_query = function(doc) {
	return {
		filters: [
			["Account", "account_type", "in", ["Cash", "Bank"]],
<<<<<<< HEAD
			["Account", "is_group", "=",0],
			["Account", "company", "=", doc.company],
			["Account", "report_type", "=", "Balance Sheet"]
=======
			["Account", "root_type", "=", "Asset"],
			["Account", "is_group", "=",0],
			["Account", "company", "=", doc.company]
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		]
	}
}

<<<<<<< HEAD
=======
cur_frm.fields_dict['supplier_address'].get_query = function(doc, cdt, cdn) {
	return{
		filters:{'supplier':  doc.supplier}
	}
}

cur_frm.fields_dict['contact_person'].get_query = function(doc, cdt, cdn) {
	return{
		filters:{'supplier':  doc.supplier}
	}
}

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
cur_frm.fields_dict['items'].grid.get_field("item_code").get_query = function(doc, cdt, cdn) {
	return {
		query: "erpnext.controllers.queries.item_query",
		filters: {'is_purchase_item': 1}
	}
}

cur_frm.fields_dict['credit_to'].get_query = function(doc) {
	// filter on Account
	if (doc.supplier) {
		return {
			filters: {
				'account_type': 'Payable',
				'is_group': 0,
				'company': doc.company
			}
		}
	} else {
		return {
			filters: {
				'report_type': 'Balance Sheet',
				'is_group': 0,
				'company': doc.company
			}
		}
	}
}

// Get Print Heading
cur_frm.fields_dict['select_print_heading'].get_query = function(doc, cdt, cdn) {
	return {
		filters:[
			['Print Heading', 'docstatus', '!=', 2]
		]
	}
}

cur_frm.set_query("expense_account", "items", function(doc) {
	return {
		query: "erpnext.controllers.queries.get_expense_account",
		filters: {'company': doc.company}
	}
});

cur_frm.set_query("asset", "items", function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	return {
		filters: {
			'item_code': d.item_code,
			'docstatus': 1,
			'company': doc.company,
			'status': 'Submitted'
		}
	}
});

cur_frm.cscript.expense_account = function(doc, cdt, cdn){
	var d = locals[cdt][cdn];
	if(d.idx == 1 && d.expense_account){
		var cl = doc.items || [];
		for(var i = 0; i < cl.length; i++){
			if(!cl[i].expense_account) cl[i].expense_account = d.expense_account;
		}
	}
	refresh_field('items');
}

cur_frm.fields_dict["items"].grid.get_field("cost_center").get_query = function(doc) {
	return {
		filters: {
			'company': doc.company,
			'is_group': 0
		}

	}
}

cur_frm.cscript.cost_center = function(doc, cdt, cdn){
	var d = locals[cdt][cdn];
	if(d.idx == 1 && d.cost_center){
		var cl = doc.items || [];
		for(var i = 0; i < cl.length; i++){
			if(!cl[i].cost_center) cl[i].cost_center = d.cost_center;
		}
	}
	refresh_field('items');
}

cur_frm.fields_dict['items'].grid.get_field('project').get_query = function(doc, cdt, cdn) {
	return{
		filters:[
			['Project', 'status', 'not in', 'Completed, Cancelled']
		]
	}
}

cur_frm.cscript.select_print_heading = function(doc,cdt,cdn){
	if(doc.select_print_heading){
		// print heading
		cur_frm.pformat.print_heading = doc.select_print_heading;
	}
	else
		cur_frm.pformat.print_heading = __("Purchase Invoice");
}

frappe.ui.form.on("Purchase Invoice", {
<<<<<<< HEAD
	setup: function(frm) {
		frm.custom_make_buttons = {
			'Purchase Invoice': 'Debit Note',
			'Payment Entry': 'Payment'
		}
	},

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	onload: function(frm) {
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
		})
	},

	is_subcontracted: function(frm) {
		if (frm.doc.is_subcontracted === "Yes") {
			erpnext.buying.get_default_bom(frm);
		}
		frm.toggle_reqd("supplier_warehouse", frm.doc.is_subcontracted==="Yes");
<<<<<<< HEAD
	},
})
=======
	}
})
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
