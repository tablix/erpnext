<<<<<<< HEAD
# Restrict Purpose Of Stock Entry


    frappe.ui.form.on("Material Request", "validate", function(frm) {
        if(frappe.user=="user1@example.com" && frm.doc.purpose!="Material Receipt") {
            frappe.msgprint("You are only allowed Material Receipt");
            frappe.throw(__("Not allowed"));
=======

    frappe.ui.form.on("Material Request", "validate", function(frm) {
        if(user=="user1@example.com" && frm.doc.purpose!="Material Receipt") {
            msgprint("You are only allowed Material Receipt");
            throw "Not allowed";
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
        }
    }


{next}
