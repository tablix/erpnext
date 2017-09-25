frappe.treeview_settings["BOM"] = {
	get_tree_nodes: 'erpnext.manufacturing.doctype.bom.bom.get_children',
	filters: [
		{
			fieldname: "bom",
			fieldtype:"Link",
			options: "BOM",
			label: __("BOM")
		}
	],
	title: "BOM",
	breadcrumb: "Manufacturing",
	disable_add_node: true,
	root_label: "bom", //fieldname from filters
	get_label: function(node) {
		if(node.data.qty) {
			return node.data.qty + " x " + node.data.item_code;
		} else {
			return node.data.item_code || node.data.value;
		}
	},
	toolbar: [
<<<<<<< HEAD
		{ toggle_btn: true },
=======
		{toggle_btn: true},
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		{
			label:__("Edit"),
			condition: function(node) {
				return node.expandable;
			},
			click: function(node) {
<<<<<<< HEAD

=======
				
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				frappe.set_route("Form", "BOM", node.data.value);
			}
		}
	],
	menu_items: [
		{
			label: __("New BOM"),
			action: function() {
				frappe.new_doc("BOM", true)
			},
			condition: 'frappe.boot.user.can_create.indexOf("BOM") !== -1'
		}
<<<<<<< HEAD
	],
	view_template: 'bom_item_preview'
=======
	]
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
}