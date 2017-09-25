// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


frappe.ui.form.on("Warehouse", {
	refresh: function(frm) {
		frm.toggle_display('warehouse_name', frm.doc.__islocal);

		frm.add_custom_button(__("Stock Balance"), function() {
			frappe.set_route("query-report", "Stock Balance", {"warehouse": frm.doc.name});
		});

		if (cint(frm.doc.is_group) == 1) {
			frm.add_custom_button(__('Group to Non-Group'),
<<<<<<< HEAD
				function() { convert_to_group_or_ledger(frm); }, 'fa fa-retweet', 'btn-default')
=======
				function() { convert_to_group_or_ledger(frm); }, 'icon-retweet', 'btn-default')
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		} else if (cint(frm.doc.is_group) == 0) {
			if(frm.doc.__onload && frm.doc.__onload.account) {
				frm.add_custom_button(__("General Ledger"), function() {
					frappe.route_options = {
						"account": frm.doc.__onload.account,
						"company": frm.doc.company
					}
					frappe.set_route("query-report", "General Ledger");
				});
			}

			frm.add_custom_button(__('Non-Group to Group'),
<<<<<<< HEAD
				function() { convert_to_group_or_ledger(frm); }, 'fa fa-retweet', 'btn-default')
		}
		
		frm.toggle_enable(['is_group', 'company'], false);
=======
				function() { convert_to_group_or_ledger(frm); }, 'icon-retweet', 'btn-default')
		}
		
		cur_frm.toggle_enable(['is_group', 'company'], false);
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

		frm.fields_dict['parent_warehouse'].get_query = function(doc) {
			return {
				filters: {
					"is_group": 1,
				}
			}
		}
<<<<<<< HEAD

		frm.fields_dict['account'].get_query = function(doc) {
			return {
				filters: {
					"is_group": 0,
					"account_type": "Stock",
					"company": frm.doc.company
				}
			}
		}
	}
});
=======
	}
});

cur_frm.set_query("create_account_under", function() {
	return {
		filters: {
			"company": cur_frm.doc.company,
			'is_group': 1
		}
	}
})
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

function convert_to_group_or_ledger(frm){
	frappe.call({
		method:"erpnext.stock.doctype.warehouse.warehouse.convert_to_group_or_ledger",
		args: {
			docname: frm.doc.name,
			is_group: frm.doc.is_group
		},
		callback: function(){
			frm.refresh();
		}
		
	})
}