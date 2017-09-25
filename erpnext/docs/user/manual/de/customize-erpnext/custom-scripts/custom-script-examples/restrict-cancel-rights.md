# Abbruchrechte einschränken
<span class="text-muted contributed-by">Beigetragen von CWT Connector & Wire Technology GmbH</span>

Fügen Sie dem Ereignis custom_before_cancel eine Steuerungsfunktion hinzu:

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
