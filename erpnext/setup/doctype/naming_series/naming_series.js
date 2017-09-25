<<<<<<< HEAD
// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt


frappe.ui.form.on("Naming Series", {
	onload: function(frm) {
		frm.disable_save();
		frm.events.get_doc_and_prefix(frm);
	},

	get_doc_and_prefix: function(frm) {
		frappe.call({
			method: "get_transactions",
			doc: frm.doc,
			callback: function(r) {
				frm.set_df_property("select_doc_for_series", "options", r.message.transactions);
				frm.set_df_property("prefix", "options", r.message.prefixes);
			}
		});
	},

	select_doc_for_series: function(frm) {
		frm.set_value("user_must_always_select", 0);
		frappe.call({
			method: "get_options",
			doc: frm.doc,
			callback: function(r) {
				frm.set_value("set_options", r.message);
				if(r.message && r.message.split('\n')[0]=='')
					frm.set_value('user_must_always_select', 1);
				frm.refresh();
			}
		});
	},

	prefix: function(frm) {
		frappe.call({
			method: "get_current",
			doc: frm.doc,
			callback: function(r) {
				frm.refresh_field("current_value");
			}
		});
	},

	update: function(frm) {
		frappe.call({
			method: "update_series",
			doc: frm.doc,
			callback: function(r) {
				frm.events.get_doc_and_prefix(frm);
			}
		});
	}
});
=======
// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


cur_frm.cscript.onload_post_render = function(doc, cdt, cdn) {
	cur_frm.disable_save();
	cur_frm.toolbar.print_icon.addClass("hide");
	return cur_frm.call({
		doc: cur_frm.doc,
		method: 'get_transactions',
		callback: function(r) {
			cur_frm.cscript.update_selects(r);
			cur_frm.cscript.select_doc_for_series(doc, cdt, cdn);
		}
	});
}

cur_frm.cscript.update_selects = function(r) {
	set_field_options('select_doc_for_series', r.message.transactions);
	set_field_options('prefix', r.message.prefixes);
}

cur_frm.cscript.select_doc_for_series = function(doc, cdt, cdn) {
	cur_frm.set_value('user_must_always_select', 0);
	cur_frm.toggle_display(['help_html','set_options', 'user_must_always_select', 'update'],
		doc.select_doc_for_series);

	var callback = function(r, rt){
		locals[cdt][cdn].set_options = r.message;
		refresh_field('set_options');
		if(r.message && r.message.split('\n')[0]=='')
			cur_frm.set_value('user_must_always_select', 1);
	}

	if(doc.select_doc_for_series)
		return $c_obj(doc,'get_options','',callback);
}

cur_frm.cscript.update = function() {
	return cur_frm.call_server('update_series', '', cur_frm.cscript.update_selects);
}

cur_frm.cscript.prefix = function(doc, dt, dn) {
	return cur_frm.call_server('get_current', '', function(r) {
		refresh_field('current_value');
	});
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
