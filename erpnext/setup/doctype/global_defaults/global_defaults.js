// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

$.extend(cur_frm.cscript, {
	validate: function(doc, cdt, cdn) {
		return $c_obj(doc, 'get_defaults', '', function(r, rt){
<<<<<<< HEAD
			frappe.sys_defaults = r.message;
=======
			sys_defaults = r.message;
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		});
	}
});
