# Anliegen der Lagerbuchung einschränken
<span class="text-muted contributed-by">Beigetragen von CWT Connector & Wire Technology GmbH</span>

    frappe.ui.form.on("Material Request", "validate", function(frm) {
        if(user=="user1@example.com" && frm.doc.purpose!="Material Receipt") {
<<<<<<< HEAD
            frappe.msgprint("You are only allowed Material Receipt");
            frappe.throw(__("Not allowed"));
=======
            msgprint("You are only allowed Material Receipt");
            throw "Not allowed";
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
        }
    }

{next}
