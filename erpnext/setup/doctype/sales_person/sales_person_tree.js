<<<<<<< HEAD

frappe.treeview_settings["Sales Person"] = {
	fields: [
		{fieldtype:'Data', fieldname: 'sales_person_name',
=======
frappe.treeview_settings["Sales Person"] = {
	fields: [
		{fieldtype:'Data', fieldname: 'name_field',
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			label:__('New Sales Person Name'), reqd:true},
		{fieldtype:'Link', fieldname:'employee',
			label:__('Employee'), options:'Employee',
			description: __("Please enter Employee Id of this sales person")},
		{fieldtype:'Check', fieldname:'is_group', label:__('Group Node'),
			description: __("Further nodes can be only created under 'Group' type nodes")}
	],
}