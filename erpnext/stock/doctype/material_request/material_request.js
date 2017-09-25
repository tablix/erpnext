// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

{% include 'erpnext/buying/doctype/purchase_common/purchase_common.js' %};

frappe.ui.form.on('Material Request', {
	setup: function(frm) {
		frm.get_field('items').grid.editable_fields = [
			{fieldname: 'item_code', columns: 2},
			{fieldname: 'qty', columns: 1},
			{fieldname: 'required_location', columns: 1},
			{fieldname: 'schedule_date', columns: 1},
			{fieldname: 'eta_date', columns: 1, allow_on_submit: true},
			{fieldname: 'substitute_item', columns: 2},
			{fieldname: 'received_quantity', columns: 1, allow_on_submit: true},
			{fieldname: 'check', columns: 1},

		];
	},
	onload: function(frm) {
		// formatter for material request item
		frm.set_indicator_formatter('item_code',
			function(doc) { return (doc.qty<=doc.ordered_qty) ? "green" : "orange" })
	}
});

frappe.ui.form.on("Material Request Item", {
	"qty": function(frm, doctype, name) {
			var d = locals[doctype][name];
			if (flt(d.qty) < flt(d.min_order_qty)) {
				alert(__("Warning: Material Requested Qty is less than Minimum Order Qty"));
			}
		}
	}
);

erpnext.buying.MaterialRequestController = erpnext.buying.BuyingController.extend({
	onload: function(doc) {
		this._super();
		this.frm.set_query("item_code", "items", function() {
			return {
				query: "erpnext.controllers.queries.item_query"
			}
		});
	},

	refresh: function(doc) {
		var me = this;
		this._super();

		if(doc.docstatus==0) {
			cur_frm.add_custom_button(__("Get Items from BOM"),
				cur_frm.cscript.get_items_from_bom, "icon-sitemap", "btn-default");
		}

		if (doc.docstatus==0 && doc.approval=="Approved")
		{
			 cur_frm.savesubmit();
		}

		if(doc.docstatus == 1 && doc.status != 'Stopped') {
			if(flt(doc.per_ordered, 2) < 100) {
				// make
				if(doc.material_request_type === "Material Transfer" && doc.status === "Submitted")
					cur_frm.add_custom_button(__("Transfer Material"),
					this.make_stock_entry, __("Make"));

				if(doc.material_request_type === "Material Issue" && doc.status === "Submitted")
					cur_frm.add_custom_button(__("Issue Material"),
					this.make_stock_entry, __("Make"));

				if(doc.material_request_type === "Purchase")
					cur_frm.add_custom_button(__('Purchase Order'),
						this.make_purchase_order, __("Make"));

				if(doc.material_request_type === "Purchase")
					cur_frm.add_custom_button(__("Request for Quotation"),
						this.make_request_for_quotation, __("Make"));

				if(doc.material_request_type === "Purchase")
					cur_frm.add_custom_button(__("Supplier Quotation"),
					this.make_supplier_quotation, __("Make"));

				if(doc.material_request_type === "Manufacture" && doc.status === "Submitted")
					cur_frm.add_custom_button(__("Production Order"),
					this.raise_production_orders, __("Make"));

				cur_frm.page.set_inner_btn_group_as_primary(__("Make"));

				// stop
				cur_frm.add_custom_button(__('Stop'),
					cur_frm.cscript['Stop Material Request']);

			}
		}

		if (this.frm.doc.docstatus===0) {
			cur_frm.add_custom_button(__('Sales Order'),
				function() {
					erpnext.utils.map_current_doc({
						method: "erpnext.selling.doctype.sales_order.sales_order.make_material_request",
						source_doctype: "Sales Order",
						get_query_filters: {
							docstatus: 1,
							status: ["!=", "Closed"],
							per_delivered: ["<", 99.99],
							company: cur_frm.doc.company
						}
					})
				}, __("Get items from"));
		}

		if(doc.docstatus == 1 && doc.status == 'Stopped')
			cur_frm.add_custom_button(__('Re-open'),
				cur_frm.cscript['Unstop Material Request']);

		// new addition
		if(doc.docstatus == 0 && doc.approval == 'Open' && frappe.user.has_role("HR User"))
			cur_frm.add_custom_button(__('Commercial Review'),
				cur_frm.cscript['Commercial Review']);

		if(doc.docstatus == 0 && doc.approval == 'Commercial Review' && frappe.user.has_role("Purchase Manager"))
		{
			cur_frm.add_custom_button(__('Approved'),
				cur_frm.cscript['Commercial Approved']);
			cur_frm.add_custom_button(__('Rejected'),
				cur_frm.cscript['Commercial Rejected']);
		}

		if(doc.customer_order && doc.upload_material_submittal && doc.assigned ==0 && doc.docstatus == 1 && doc.approval == 'Approved'  && frappe.user.has_role("Projects User"))
		{
			cur_frm.add_custom_button(__('Send to Commercial'),
				cur_frm.cscript['Commercial Review']);
		}

		if(doc.docstatus == 0 && (doc.approval == 'Commercial Rejected' || doc.approval == "KAM Rejected") && frappe.user.has_role("Projects User"))
		{
			cur_frm.add_custom_button(__('Commercial Review'),
				cur_frm.cscript['Commercial Review']);
			//cur_frm.add_custom_button(__('KAM Approval'),
			//	cur_frm.cscript['KAM Review']);
		}
		if(doc.docstatus == 0 && doc.approval == 'KAM Review' && (frappe.user.has_role("CEO") || frappe.user.has_role("CBDO")))
		{
			cur_frm.add_custom_button(__('KAM Approve'),
				cur_frm.cscript['KAM Approve']);
			cur_frm.add_custom_button(__('KAM Reject'),
				cur_frm.cscript['KAM Reject']);
		}

		if(doc.reason != "" || doc.reason != null )
		{
			cur_frm.set_intro(__(cur_frm.doc.reason));
		}


	},


	schedule_date: function(doc, cdt, cdn) {
		var val = locals[cdt][cdn].schedule_date;
		if(val) {
			$.each((doc.items || []), function(i, d) {
				if(!d.schedule_date) {
					d.schedule_date = val;
				}
			});
			refresh_field("items");
		}
	},

	get_items_from_bom: function() {
		var d = new frappe.ui.Dialog({
			title: __("Get Items from BOM"),
			fields: [
				{"fieldname":"bom", "fieldtype":"Link", "label":__("BOM"),
					options:"BOM", reqd: 1, get_query: function(){
						return {filters: { docstatus:1 }}
					}},
				{"fieldname":"warehouse", "fieldtype":"Link", "label":__("Warehouse"),
					options:"Warehouse", reqd: 1, label:"For Warehouse"},
				{"fieldname":"fetch_exploded", "fieldtype":"Check",
					"label":__("Fetch exploded BOM (including sub-assemblies)"), "default":1},
				{fieldname:"fetch", "label":__("Get Items from BOM"), "fieldtype":"Button"}
			]
		});
		d.get_input("fetch").on("click", function() {
			var values = d.get_values();
			if(!values) return;
			values["company"] = cur_frm.doc.company;
			frappe.call({
				method: "erpnext.manufacturing.doctype.bom.bom.get_bom_items",
				args: values,
				callback: function(r) {
					if(!r.message) {
						frappe.throw(__("BOM does not contain any stock item"))
					} else {
						$.each(r.message, function(i, item) {
							var d = frappe.model.add_child(cur_frm.doc, "Material Request Item", "items");
							d.item_code = item.item_code;
							d.description = item.description;
							d.warehouse = values.warehouse;
							d.uom = item.stock_uom;
							d.qty = item.qty;
						});
					}
					d.hide();
					refresh_field("items");
				}
			});
		});
		d.show();
	},

	tc_name: function() {
		this.get_terms();
	},

	validate_company_and_party: function(party_field) {
		return true;
	},

	calculate_taxes_and_totals: function() {
		return;
	},

	make_purchase_order: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.stock.doctype.material_request.material_request.make_purchase_order",
			frm: cur_frm,
			run_link_triggers: true
		});
	},

	make_request_for_quotation: function(){
		frappe.model.open_mapped_doc({
			method: "erpnext.stock.doctype.material_request.material_request.make_request_for_quotation",
			frm: cur_frm,
			run_link_triggers: true
		});
	},

	make_supplier_quotation: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.stock.doctype.material_request.material_request.make_supplier_quotation",
			frm: cur_frm
		});
	},

	make_stock_entry: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.stock.doctype.material_request.material_request.make_stock_entry",
			frm: cur_frm
		});
	},

	raise_production_orders: function() {
		frappe.call({
			method:"erpnext.stock.doctype.material_request.material_request.raise_production_orders",
			args: {
				"material_request": cur_frm.doc.name
			}
		});
	},
	//new addition
	check_all: function() {
		cur_frm.cscript.check_all();
	},

	uncheck_all: function() {
		cur_frm.cscript.uncheck_all();
	},

	delete: function() {
		cur_frm.cscript.delete_all();
	}


});

// for backward compatibility: combine new and previous states
$.extend(cur_frm.cscript, new erpnext.buying.MaterialRequestController({frm: cur_frm}));

cur_frm.cscript['Stop Material Request'] = function() {
	var doc = cur_frm.doc;
	$c('runserverobj', args={'method':'update_status', 'arg': 'Stopped', 'docs': doc}, function(r,rt) {
		cur_frm.refresh();
	});
};

cur_frm.cscript['Unstop Material Request'] = function(){
	var doc = cur_frm.doc;
	$c('runserverobj', args={'method':'update_status', 'arg': 'Submitted','docs': doc}, function(r,rt) {
		cur_frm.refresh();
	});
};



//new addition

cur_frm.cscript['Commercial Review']=function()
{

	return cur_frm.call({
				doc: cur_frm.doc,
				method: "send_notification",
				args: "cm_review",
				callback: function(r) {
					if(r.exc) {
						msgprint(__("There were errors."));
					} else {
						msgprint(__("Succesfully send to the respected tablix rep !!!!!"));
						cur_frm.timeline.insert_comment("Workflow", "MR sent for Commercial review");
						location.reload();
					}
				}
			});

}
cur_frm.cscript['Commercial Approved']=function()
{

	return cur_frm.call({
				doc: cur_frm.doc,
				method: "send_notification",
				args: "cm_approved",
				callback: function(r) {
					if(r.exc) {
						msgprint(__("There were errors."));
					} else {
						msgprint(__("Succesfully send to the respected tablix rep !!!!!"));
						cur_frm.timeline.insert_comment("Workflow", "MR approved by Commercial Team");
						location.reload();
					}
				}
			});

}
cur_frm.cscript['Commercial Rejected']=function()
{
	var dialog = new frappe.ui.Dialog({
		title: "Rejected with Remark",
		fields: [
			{"fieldtype": "Text", "label": __("Remarks"), "fieldname": "reason",
				"reqd": 1 },
			{"fieldtype": "Button", "label": __("Send"), "fieldname": "finish"},
		]

	});
	dialog.show();

	dialog.fields_dict.finish.$input.click(function() {
		arg = dialog.get_values();
		if(!arg) return;
		var reason = arg.reason;
		return cur_frm.call({
			doc: cur_frm.doc,
			method: "send_notification",
			args: {"reason": "cm_rejected", "remark": reason},
			callback: function(r) {
				if(r.exc) {
					dialog.hide();
					msgprint(__("There were errors."));
				} else {
					dialog.hide();
					cur_frm.timeline.insert_comment("Workflow", "MR rejected by Commercial Team");
					msgprint(__("Succesfully send to respective project engg/manager !!!!!"));
					location.reload();
				}
			}
		});
	});

}

cur_frm.cscript['KAM Review']=function()
{

	return cur_frm.call({
				doc: cur_frm.doc,
				method: "send_notification",
				args: "kam_review",
				callback: function(r) {
					if(r.exc) {
						msgprint(__("There were errors."));
					} else {
						msgprint(__("Succesfully send to the respected tablix rep !!!!!"));
						cur_frm.timeline.insert_comment("Workflow", "MR sent for Account Manager review");
						location.reload();
					}
				}
			});

}

cur_frm.cscript['KAM Approve']=function()
{
	alert("success!!")
	return cur_frm.call({
				doc: cur_frm.doc,
				method: "send_notification",
				args: "kam_approved",
				callback: function(r) {
					if(r.exc) {
						msgprint(__("There were errors."));
					} else {
						msgprint(__("Succesfully send to the respected tablix rep !!!!!"));
						cur_frm.timeline.insert_comment("Workflow", "MR approved by KAM");
						location.reload();
					}
				}
			});

}

cur_frm.cscript['KAM Reject']=function()
{
	var dialog = new frappe.ui.Dialog({
	title: "Rejected with Remark",
	fields: [
		{"fieldtype": "Text", "label": __("Remarks"), "fieldname": "reason",
			"reqd": 1 },
		{"fieldtype": "Button", "label": __("Send"), "fieldname": "finish"},
	]

	});
	dialog.show();

	dialog.fields_dict.finish.$input.click(function() {
		arg = dialog.get_values();
		if(!arg) return;
		var reason = arg.reason;
		return cur_frm.call({
			doc: cur_frm.doc,
			method: "send_notification",
			args: {"reason": "kam_rejected", "remark": reason},
			callback: function(r) {
				if(r.exc) {
					dialog.hide();
					msgprint(__("There were errors."));
				} else {
					dialog.hide();
					cur_frm.timeline.insert_comment("Workflow", "MR rejected by KAM");
					msgprint(__("Succesfully send to respective project engg/manager !!!!!"));
					location.reload();
				}
			}
		});
	});
}

//new addition

cur_frm.cscript.check_all = function(){
	var rm = cur_frm.doc.items || [];
	for(var i=0;i<rm.length;i++)
	{
		set_multiple('Material Request Item',rm[i].name, {'check': 1}, 'items');
	}
}

cur_frm.cscript.uncheck_all = function(){
	var rm = cur_frm.doc.items || [];
	for(var i=0;i<rm.length;i++)
	{
		set_multiple('Material Request Item',rm[i].name, {'check': 0}, 'items');
	}
}

cur_frm.cscript.delete_all = function()
{
	var tbl = cur_frm.doc.items || [];
	var i = tbl.length;
	while (i--)
	{
		if(tbl[i].check == 1)
		{
         cur_frm.get_field("items").grid.grid_rows[i].remove();
		}
	}

}
