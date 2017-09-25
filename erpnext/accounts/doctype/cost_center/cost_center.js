// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.accounts");



frappe.ui.form.on('Cost Center', {
	onload: function(frm) {
		frm.set_query("parent_cost_center", function() {
			return {
				filters: {
					company: frm.doc.company,
					is_group: 1
				}
			}
		})
	}
})

cur_frm.cscript.refresh = function(doc, cdt, cdn) {
	var intro_txt = '';
	cur_frm.toggle_display('cost_center_name', doc.__islocal);
	cur_frm.toggle_enable(['is_group', 'company'], doc.__islocal);

	if(!doc.__islocal && doc.is_group==1) {
		intro_txt += __('Note: This Cost Center is a Group. Cannot make accounting entries against groups.');
	}

	cur_frm.cscript.hide_unhide_group_ledger(doc);

	cur_frm.toggle_display('sb1', doc.is_group==0)
	cur_frm.set_intro(intro_txt);

	if(!cur_frm.doc.__islocal) {
		cur_frm.add_custom_button(__('Chart of Cost Centers'),
			function() { frappe.set_route("Tree", "Cost Center"); });

		cur_frm.add_custom_button(__('Budget'),
			function() { frappe.set_route("List", "Budget", {'cost_center': cur_frm.doc.name}); });
	}
}

cur_frm.cscript.parent_cost_center = function(doc, cdt, cdn) {
	if(!doc.company){
<<<<<<< HEAD
		frappe.msgprint(__('Please enter company name first'));
=======
		msgprint(__('Please enter company name first'));
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	}
}

cur_frm.cscript.hide_unhide_group_ledger = function(doc) {
	if (doc.is_group == 1) {
		cur_frm.add_custom_button(__('Convert to Non-Group'),
<<<<<<< HEAD
			function() { cur_frm.cscript.convert_to_ledger(); }, "fa fa-retweet",
				"btn-default")
	} else if (doc.is_group == 0) {
		cur_frm.add_custom_button(__('Convert to Group'),
			function() { cur_frm.cscript.convert_to_group(); }, "fa fa-retweet",
=======
			function() { cur_frm.cscript.convert_to_ledger(); }, "icon-retweet",
				"btn-default")
	} else if (doc.is_group == 0) {
		cur_frm.add_custom_button(__('Convert to Group'),
			function() { cur_frm.cscript.convert_to_group(); }, "icon-retweet",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				"btn-default")
	}
}

cur_frm.cscript.convert_to_ledger = function(doc, cdt, cdn) {
	return $c_obj(cur_frm.doc,'convert_group_to_ledger','',function(r,rt) {
		if(r.message == 1) {
			cur_frm.refresh();
		}
	});
}

cur_frm.cscript.convert_to_group = function(doc, cdt, cdn) {
	return $c_obj(cur_frm.doc,'convert_ledger_to_group','',function(r,rt) {
		if(r.message == 1) {
			cur_frm.refresh();
		}
	});
}
