// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

<<<<<<< HEAD
erpnext.SMSManager = function SMSManager(doc) {
=======
function SMSManager(doc) {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	var me = this;
	this.setup = function() {
		var default_msg = {
			'Lead'				: '',
			'Opportunity'			: 'Your enquiry has been logged into the system. Ref No: ' + doc.name,
			'Quotation'			: 'Quotation ' + doc.name + ' has been sent via email. Thanks!',
			'Sales Order'		: 'Sales Order ' + doc.name + ' has been created against '
						+ (doc.quotation_no ? ('Quote No:' + doc.quotation_no) : '')
						+ (doc.po_no ? (' for your PO: ' + doc.po_no) : ''),
			'Delivery Note'		: 'Items has been delivered against delivery note: ' + doc.name
						+ (doc.po_no ? (' for your PO: ' + doc.po_no) : ''),
			'Sales Invoice': 'Invoice ' + doc.name + ' has been sent via email '
						+ (doc.po_no ? (' for your PO: ' + doc.po_no) : ''),
			'Material Request'			: 'Material Request ' + doc.name + ' has been raised in the system',
			'Purchase Order'	: 'Purchase Order ' + doc.name + ' has been sent via email',
			'Purchase Receipt'	: 'Items has been received against purchase receipt: ' + doc.name
		}

		if (in_list(['Quotation', 'Sales Order', 'Delivery Note', 'Sales Invoice'], doc.doctype))
<<<<<<< HEAD
			this.show(doc.contact_person, 'Customer', doc.customer, '', default_msg[doc.doctype]);
		else if (in_list(['Purchase Order', 'Purchase Receipt'], doc.doctype))
			this.show(doc.contact_person, 'Supplier', doc.supplier, '', default_msg[doc.doctype]);
=======
			this.show(doc.contact_person, 'customer', doc.customer, '', default_msg[doc.doctype]);
		else if (in_list(['Purchase Order', 'Purchase Receipt'], doc.doctype))
			this.show(doc.contact_person, 'supplier', doc.supplier, '', default_msg[doc.doctype]);
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		else if (doc.doctype == 'Lead')
			this.show('', '', '', doc.mobile_no, default_msg[doc.doctype]);
		else if (doc.doctype == 'Opportunity')
			this.show('', '', '', doc.contact_no, default_msg[doc.doctype]);
		else if (doc.doctype == 'Material Request')
			this.show('', '', '', '', default_msg[doc.doctype]);

	};

<<<<<<< HEAD
	this.get_contact_number = function(contact, ref_doctype, ref_name) {
		frappe.call({
			method: "frappe.core.doctype.sms_settings.sms_settings.get_contact_number",
			args: {
				contact_name: contact,
				ref_doctype: ref_doctype,
				ref_name: ref_name
			},
			callback: function(r) {
				if(r.exc) { frappe.msgprint(r.exc); return; }
=======
	this.get_contact_number = function(contact, key, value) {
		frappe.call({
			method: "erpnext.setup.doctype.sms_settings.sms_settings.get_contact_number",
			args: {
				contact_name:contact,
				value:value,
				key:key
			},
			callback: function(r) {
				if(r.exc) { msgprint(r.exc); return; }
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				me.number = r.message;
				me.show_dialog();
			}
		});
	};

<<<<<<< HEAD
	this.show = function(contact, ref_doctype, ref_name, mobile_nos, message) {
=======
	this.show = function(contact, key, value, mobile_nos, message) {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		this.message = message;
		if (mobile_nos) {
			me.number = mobile_nos;
			me.show_dialog();
		} else if (contact){
<<<<<<< HEAD
			this.get_contact_number(contact, ref_doctype, ref_name)
=======
			this.get_contact_number(contact, key, value)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		} else {
			me.show_dialog();
		}
	}
	this.show_dialog = function() {
		if(!me.dialog)
			me.make_dialog();
		me.dialog.set_values({
			'message': me.message,
			'number': me.number
		})
		me.dialog.show();
	}
	this.make_dialog = function() {
		var d = new frappe.ui.Dialog({
			title: 'Send SMS',
			width: 400,
			fields: [
				{fieldname:'number', fieldtype:'Data', label:'Mobile Number', reqd:1},
				{fieldname:'message', fieldtype:'Text', label:'Message', reqd:1},
				{fieldname:'send', fieldtype:'Button', label:'Send'}
			]
		})
		d.fields_dict.send.input.onclick = function() {
			var btn = d.fields_dict.send.input;
			var v = me.dialog.get_values();
			if(v) {
				$(btn).set_working();
				frappe.call({
<<<<<<< HEAD
					method: "frappe.core.doctype.sms_settings.sms_settings.send_sms",
=======
					method: "erpnext.setup.doctype.sms_settings.sms_settings.send_sms",
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
					args: {
						receiver_list: [v.number],
						msg: v.message
					},
					callback: function(r) {
						$(btn).done_working();
<<<<<<< HEAD
						if(r.exc) {frappe.msgprint(r.exc); return; }
=======
						if(r.exc) {msgprint(r.exc); return; }
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
						me.dialog.hide();
					}
				});
			}
		}
		this.dialog = d;
	}
	this.setup();
}
