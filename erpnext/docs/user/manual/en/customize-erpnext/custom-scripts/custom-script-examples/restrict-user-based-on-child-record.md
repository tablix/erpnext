<<<<<<< HEAD
# Restrict User Based On Child Record


    // restrict certain warehouse to Material Manager
    cur_frm.cscript.custom_validate = function(doc) {
        if(frappe.user_roles.indexOf("Material Manager")==-1) {

            var restricted_in_source = frappe.model.get_list("Stock Entry Detail",
                {parent:cur_frm.doc.name, s_warehouse:"Restricted"});

            var restricted_in_target = frappe.model.get_list("Stock Entry Detail",
                {parent:cur_frm.doc.name, t_warehouse:"Restricted"})

            if(restricted_in_source.length || restricted_in_target.length) {
                frappe.msgprint(__("Only Material Manager can make entry in Restricted Warehouse"));
=======

    // restrict certain warehouse to Material Manager
    cur_frm.cscript.custom_validate = function(doc) {
        if(user_roles.indexOf("Material Manager")==-1) {

            var restricted_in_source = wn.model.get("Stock Entry Detail",
                {parent:cur_frm.doc.name, s_warehouse:"Restricted"});

            var restricted_in_target = wn.model.get("Stock Entry Detail",
                {parent:cur_frm.doc.name, t_warehouse:"Restricted"})

            if(restricted_in_source.length || restricted_in_target.length) {
                msgprint("Only Material Manager can make entry in Restricted Warehouse");
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
                validated = false;
            }
        }
    }


{next}
