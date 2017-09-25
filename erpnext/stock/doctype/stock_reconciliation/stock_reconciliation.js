// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.stock");

frappe.ui.form.on("Stock Reconciliation", {
	onload: function(frm) {
		frm.add_fetch("item_code", "item_name", "item_name");

		// end of life
		frm.set_query("item_code", "items", function(doc, cdt, cdn) {
			return {
				query: "erpnext.controllers.queries.item_query",
				filters:{
					"is_stock_item": 1,
					"has_serial_no": 0
				}
			}
		});

		if (frm.doc.company) {
			erpnext.queries.setup_queries(frm, "Warehouse", function() {
				return erpnext.queries.warehouse(frm.doc);
			});
		}
	},

	refresh: function(frm) {
		if(frm.doc.docstatus < 1) {
			frm.add_custom_button(__("Items"), function() {
				frm.events.get_items(frm);
			});
		}
<<<<<<< HEAD

		if(frm.doc.company) {
			frm.trigger("toggle_display_account_head");
		}
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	},

	get_items: function(frm) {
		frappe.prompt({label:"Warehouse", fieldtype:"Link", options:"Warehouse", reqd: 1},
			function(data) {
				frappe.call({
					method:"erpnext.stock.doctype.stock_reconciliation.stock_reconciliation.get_items",
					args: {
						warehouse: data.warehouse,
						posting_date: frm.doc.posting_date,
						posting_time: frm.doc.posting_time
					},
					callback: function(r) {
						var items = [];
						frm.clear_table("items");
						for(var i=0; i< r.message.length; i++) {
							var d = frm.add_child("items");
							$.extend(d, r.message[i]);
							if(!d.qty) d.qty = null;
							if(!d.valuation_rate) d.valuation_rate = null;
						}
						frm.refresh_field("items");
					}
				});
			}
		, __("Get Items"), __("Update"));
	},

	set_valuation_rate_and_qty: function(frm, cdt, cdn) {
		var d = frappe.model.get_doc(cdt, cdn);
		if(d.item_code && d.warehouse) {
			frappe.call({
				method: "erpnext.stock.doctype.stock_reconciliation.stock_reconciliation.get_stock_balance_for",
				args: {
					item_code: d.item_code,
					warehouse: d.warehouse,
					posting_date: frm.doc.posting_date,
					posting_time: frm.doc.posting_time
				},
				callback: function(r) {
					frappe.model.set_value(cdt, cdn, "qty", r.message.qty);
					frappe.model.set_value(cdt, cdn, "valuation_rate", r.message.rate);
					frappe.model.set_value(cdt, cdn, "current_qty", r.message.qty);
					frappe.model.set_value(cdt, cdn, "current_valuation_rate", r.message.rate);
<<<<<<< HEAD
					frappe.model.set_value(cdt, cdn, "current_amount", r.message.rate * r.message.qty);
					frappe.model.set_value(cdt, cdn, "amount", r.message.rate * r.message.qty);

				}
			});
		}
	},
	set_item_code: function(doc, cdt, cdn) {
		var d = frappe.model.get_doc(cdt, cdn);
		if (d.barcode) {
			frappe.call({
				method: "erpnext.stock.get_item_details.get_item_code",
				args: {"barcode": d.barcode },
				callback: function(r) {
					if (!r.exe){
						frappe.model.set_value(cdt, cdn, "item_code", r.message);
					}
				}
			});
		}
	},
	set_amount_quantity: function(doc, cdt, cdn) {
		var d = frappe.model.get_doc(cdt, cdn);
		if (d.qty & d.valuation_rate) {
			frappe.model.set_value(cdt, cdn, "amount", flt(d.qty) * flt(d.valuation_rate));
			frappe.model.set_value(cdt, cdn, "quantity_difference", flt(d.qty) - flt(d.current_qty));
			frappe.model.set_value(cdt, cdn, "amount_difference", flt(d.amount) - flt(d.current_amount));
		}
	},
	company: function(frm) {
		frm.trigger("toggle_display_account_head");
	},
	toggle_display_account_head: function(frm) {
		frm.toggle_display(['expense_account', 'cost_center'],
			erpnext.is_perpetual_inventory_enabled(frm.doc.company));
=======
				}
			});
		}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	}
});

frappe.ui.form.on("Stock Reconciliation Item", {
<<<<<<< HEAD
	barcode: function(frm, cdt, cdn) {
		frm.events.set_item_code(frm, cdt, cdn);
	},
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	warehouse: function(frm, cdt, cdn) {
		frm.events.set_valuation_rate_and_qty(frm, cdt, cdn);
	},
	item_code: function(frm, cdt, cdn) {
		frm.events.set_valuation_rate_and_qty(frm, cdt, cdn);
<<<<<<< HEAD
	},
	qty: function(frm, cdt, cdn) {
		frm.events.set_amount_quantity(frm, cdt, cdn);
	},
	valuation_rate: function(frm, cdt, cdn) {
		frm.events.set_amount_quantity(frm, cdt, cdn);
	}

=======
	}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
});

erpnext.stock.StockReconciliation = erpnext.stock.StockController.extend({
	onload: function() {
		this.set_default_expense_account();
	},

	set_default_expense_account: function() {
		var me = this;
		if(this.frm.doc.company) {
<<<<<<< HEAD
			if (erpnext.is_perpetual_inventory_enabled(this.frm.doc.company) && !this.frm.doc.expense_account) {
=======
			if (sys_defaults.auto_accounting_for_stock && !this.frm.doc.expense_account) {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				return this.frm.call({
					method: "erpnext.accounts.utils.get_company_default",
					args: {
						"fieldname": "stock_adjustment_account",
						"company": this.frm.doc.company
					},
					callback: function(r) {
						if (!r.exc) {
							me.frm.set_value("expense_account", r.message);
						}
					}
				});
			}
		}
	},

	setup: function() {
		var me = this;
<<<<<<< HEAD

		this.setup_posting_date_time_check();

		if (me.frm.doc.company && erpnext.is_perpetual_inventory_enabled(me.frm.doc.company)) {
			this.frm.add_fetch("company", "stock_adjustment_account", "expense_account");
			this.frm.add_fetch("company", "cost_center", "cost_center");
		}
		this.frm.fields_dict["expense_account"].get_query = function() {
			if(erpnext.is_perpetual_inventory_enabled(me.frm.doc.company)) {
=======
		this.frm.get_docfield("items").allow_bulk_edit = 1;

		if (sys_defaults.auto_accounting_for_stock) {
			this.frm.add_fetch("company", "stock_adjustment_account", "expense_account");
			this.frm.add_fetch("company", "cost_center", "cost_center");

			this.frm.fields_dict["expense_account"].get_query = function() {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				return {
					"filters": {
						'company': me.frm.doc.company,
						"is_group": 0
					}
				}
			}
<<<<<<< HEAD
		}
		this.frm.fields_dict["cost_center"].get_query = function() {
			if(erpnext.is_perpetual_inventory_enabled(me.frm.doc.company)) {
=======
			this.frm.fields_dict["cost_center"].get_query = function() {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				return {
					"filters": {
						'company': me.frm.doc.company,
						"is_group": 0
					}
				}
			}
		}
<<<<<<< HEAD
=======

		this.frm.get_field('items').grid.editable_fields = [
			{fieldname: 'item_code', columns: 3},
			{fieldname: 'warehouse', columns: 3},
			{fieldname: 'qty', columns: 2},
			{fieldname: 'valuation_rate', columns: 2}
		];
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	},

	refresh: function() {
		if(this.frm.doc.docstatus==1) {
			this.show_stock_ledger();
<<<<<<< HEAD
			if (erpnext.is_perpetual_inventory_enabled(this.frm.doc.company)) {
=======
			if (cint(frappe.defaults.get_default("auto_accounting_for_stock"))) {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				this.show_general_ledger();
			}
		}
	},

});

cur_frm.cscript = new erpnext.stock.StockReconciliation({frm: cur_frm});
