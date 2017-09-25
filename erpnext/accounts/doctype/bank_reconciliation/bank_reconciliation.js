// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on("Bank Reconciliation", {
	setup: function(frm) {
<<<<<<< HEAD
		frm.add_fetch("bank_account", "account_currency", "account_currency");
	},

	onload: function(frm) {

		let default_bank_account =  frappe.defaults.get_user_default("Company")? 
			locals[":Company"][frappe.defaults.get_user_default("Company")]["default_bank_account"]: "";
=======
		frm.get_docfield("payment_entries").allow_bulk_edit = 1;
		frm.add_fetch("bank_account", "account_currency", "account_currency");

		frm.get_field('payment_entries').grid.editable_fields = [
			{fieldname: 'against_account', columns: 3},
			{fieldname: 'amount', columns: 2},
			{fieldname: 'cheque_number', columns: 3},
			{fieldname: 'clearance_date', columns: 2}
		];
	},

	onload: function(frm) {
		var default_bank_account =  locals[":Company"][frappe.defaults.get_user_default("Company")]["default_bank_account"];

>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		frm.set_value("bank_account", default_bank_account);

		frm.set_query("bank_account", function() {
			return {
				"filters": {
<<<<<<< HEAD
					"account_type": ["in",["Bank","Cash"]],
=======
					"account_type": "Bank",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
					"is_group": 0
				}
			};
		});

		frm.set_value("from_date", frappe.datetime.month_start());
		frm.set_value("to_date", frappe.datetime.month_end());
	},

	refresh: function(frm) {
		frm.disable_save();
	},

	update_clearance_date: function(frm) {
		return frappe.call({
			method: "update_clearance_date",
			doc: frm.doc,
			callback: function(r, rt) {
				frm.refresh_field("payment_entries");
				frm.refresh_fields();
			}
		});
	},
	get_payment_entries: function(frm) {
		return frappe.call({
			method: "get_payment_entries",
			doc: frm.doc,
			callback: function(r, rt) {
				frm.refresh_field("payment_entries");
				frm.refresh_fields();
<<<<<<< HEAD

				$(frm.fields_dict.payment_entries.wrapper).find("[data-fieldname=amount]").each(function(i,v){
					if (i !=0){
						$(v).addClass("text-right")
					}
				})
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			}
		});
	}
});
