<<<<<<< HEAD
# Restrict Cancel Rights

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
Add a handler to `custom_before_cancel` event:



    cur_frm.cscript.custom_before_cancel = function(doc) {
<<<<<<< HEAD
        if (frappe.user_roles.indexOf("Accounts User")!=-1 && frappe.user_roles.indexOf("Accounts Manager")==-1
                && user_roles.indexOf("System Manager")==-1) {
            if (flt(doc.grand_total) > 10000) {
                frappe.msgprint("You can not cancel this transaction, because grand total \
                    is greater than 10000");
                frappe.validated = false;
=======
        if (user_roles.indexOf("Accounts User")!=-1 && user_roles.indexOf("Accounts Manager")==-1
                && user_roles.indexOf("System Manager")==-1) {
            if (flt(doc.grand_total) > 10000) {
                msgprint("You can not cancel this transaction, because grand total \
                    is greater than 10000");
                validated = false;
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
            }
        }
    }


{next}
