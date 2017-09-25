// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

<<<<<<< HEAD
cur_frm.cscript.onload = function (doc, dt, dn) {
	if (!doc.posting_date)
		set_multiple(dt, dn, { posting_date: frappe.datetime.get_today() });
	if (!doc.leave_transaction_type)
		set_multiple(dt, dn, { leave_transaction_type: 'Allocation' });
}

cur_frm.cscript.to_date = function (doc, cdt, cdn) {
	return $c('runserverobj', { 'method': 'to_date_validation', 'docs': doc },
		function (r, rt) {
			var doc = locals[cdt][cdn];
			if (r.message) {
				frappe.msgprint(__("To date cannot be before from date"));
=======
cur_frm.cscript.onload = function(doc, dt, dn){
	if(!doc.posting_date)
		set_multiple(dt, dn, {posting_date: get_today()});
	if(!doc.leave_transaction_type)
		set_multiple(dt, dn, {leave_transaction_type: 'Allocation'});
}

cur_frm.cscript.to_date = function(doc, cdt, cdn) {
	return $c('runserverobj', args={'method':'to_date_validation','docs':doc},
		function(r, rt) {
			var doc = locals[cdt][cdn];
			if (r.message) {
				msgprint(__("To date cannot be before from date"));
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				doc.to_date = '';
				refresh_field('to_date');
			}
		}
	);
}

<<<<<<< HEAD
cur_frm.cscript.allocation_type = function (doc, cdt, cdn) {
=======
cur_frm.cscript.allocation_type = function (doc, cdt, cdn){
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	doc.no_of_days = '';
	refresh_field('no_of_days');
}

<<<<<<< HEAD
frappe.ui.form.on("Leave Control Panel", "refresh", function (frm) {
=======
frappe.ui.form.on("Leave Control Panel", "refresh", function(frm) {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	frm.disable_save();
});