<<<<<<< HEAD
# Update Date Field Based On Value In Other Date Field

=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
Below script would auto-set value for the date field, based on the value in another date field.

Example: Production Due Date must be set as two days before Delivery Date. If you have Production Due Date field already, with field type as Date, as per the below given script, date will be auto-updated in it, two days prior Deliver Date.

    cur_frm.cscript.custom_delivery_date = function(doc, cdt, cd){
    cur_frm.set_value("production_due_date", frappe.datetime.add_days(doc.delivery_date, -2));
     }
