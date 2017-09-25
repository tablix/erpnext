// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

<<<<<<< HEAD
frappe.ui.form.on("Workstation", {
	onload: function(frm) {
		if(frm.is_new())
		{
			frappe.call({
				type:"GET",
				method:"erpnext.manufacturing.doctype.workstation.workstation.get_default_holiday_list",
				callback: function(r) {
					if(!r.exe && r.message){
						cur_frm.set_value("holiday_list", r.message);
					}
				}
			})
		}
	}
})
=======


//--------- ONLOAD -------------
cur_frm.cscript.onload = function(doc, cdt, cdn) {
	frappe.call({
		type:"GET",
		method:"erpnext.manufacturing.doctype.workstation.workstation.get_default_holiday_list",
		callback: function(r) {
			if(!r.exe && r.message){
				cur_frm.set_value("holiday_list", r.message);
			}
		}
	})
}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
