// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.crm");

cur_frm.email_field = "contact_email";
frappe.ui.form.on("Opportunity", {
	customer: function(frm) {
		erpnext.utils.get_party_details(frm);
	},
	customer_address: function(frm, cdt, cdn){
		erpnext.utils.get_address_display(frm, 'customer_address', 'address_display', false);
	},
	contact_person: erpnext.utils.get_contact_details,
	enquiry_from: function(frm) {
		frm.toggle_reqd("lead", frm.doc.enquiry_from==="Lead");
		frm.toggle_reqd("customer", frm.doc.enquiry_from==="Customer");
	},
	refresh: function(frm) {
		frm.events.enquiry_from(frm);
	}
})

// TODO commonify this code
erpnext.crm.Opportunity = frappe.ui.form.Controller.extend({
	onload: function() {
		
		if(!this.frm.doc.enquiry_from && this.frm.doc.customer)
			this.frm.doc.enquiry_from = "Customer";
		if(!this.frm.doc.enquiry_from && this.frm.doc.lead)
			this.frm.doc.enquiry_from = "Lead";

		//if(!this.frm.doc.status)
		//	set_multiple(cdt, cdn, { status:'Draft' });
		if(!this.frm.doc.company && frappe.defaults.get_user_default("Company"))
			set_multiple(cdt, cdn, { company:frappe.defaults.get_user_default("Company") });

		this.setup_queries();
	},

	setup_queries: function() {
		var me = this;

		if(this.frm.fields_dict.contact_by.df.options.match(/^User/)) {
			this.frm.set_query("contact_by", erpnext.queries.user);
		}

		this.frm.set_query("customer_address", function() {
			if(me.frm.doc.lead) return {filters: { lead: me.frm.doc.lead } };
			else if(me.frm.doc.customer) return {filters: { customer: me.frm.doc.customer } };
		});

		this.frm.set_query("item_code", "items", function() {
			return {
				query: "erpnext.controllers.queries.item_query",
				filters: {'is_sales_item': 1}
			};
		});

		$.each([["lead", "lead"],
			["customer", "customer"],
			["contact_person", "customer_filter"],
			["territory", "not_a_group_filter"]], function(i, opts) {
				me.frm.set_query(opts[0], erpnext.queries[opts[1]]);
			});
	},

	create_quotation: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.crm.doctype.opportunity.opportunity.make_quotation",
			frm: cur_frm
		})
	},
	
	//new addition
	
	create_boq: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.crm.doctype.opportunity.opportunity.make_boq",
			frm: cur_frm
		})
		cur_frm.timeline.insert_comment("Workflow", "Converted to BOQ");
	}
	
	//new addition
	
	
});

$.extend(cur_frm.cscript, new erpnext.crm.Opportunity({frm: cur_frm}));

cur_frm.cscript.refresh = function(doc, cdt, cdn) {
	erpnext.toggle_naming_series();

	var frm = cur_frm;

	if(doc.__islocal)
	{
		frm.set_value("status", "Open")
	}
	//frm.set_df_property("status", "read_only", frm.doc.__islocal ? 0 : 1);
	
	//new addition
	
	var df = frappe.meta.get_docfield("Compliance", "technical_compliance", cur_frm.doc.name);
	df.read_only = 1;
	var df = frappe.meta.get_docfield("Compliance", "commercial_compliance", cur_frm.doc.name);
	df.read_only = 1;
	
	if(frm.doc.status == "Open")
	{
		cur_frm.add_custom_button(__('Send for Approval'),
			cur_frm.cscript['Send for Approval']);
	}		
	
	
	if((frappe.user.has_role("Security") || frappe.user.has_role("AV") || frappe.user.has_role("BMS") || frappe.user.has_role("Business Automation"))  && (frm.doc.status == "Boq" || frm.doc.status == "RFQ Approved"))
	{
		cur_frm.add_custom_button(__('BoQ'),
			cur_frm.cscript.create_boq)
		cur_frm.add_custom_button(__('Need more info'),
			cur_frm.cscript['Insufficient Info']);
			
	}	
	if((frappe.user.has_role("CEO") || frappe.user.has_role("CBDO")) && (frm.doc.status == "Rfq" || frm.doc.status == "RFQ"))
	{
		cur_frm.add_custom_button(__('KAM Approve'), 
			cur_frm.cscript['SAM Approval']);
		cur_frm.add_custom_button(__('Need more info'), 
			cur_frm.cscript['Insufficient Info']);
	}
	if(frappe.user.has_role("COO") && frm.doc.status == "KAM Approved")
	{
		cur_frm.add_custom_button(__('COO Approve'), 
			cur_frm.cscript['COO Approval']);
		cur_frm.add_custom_button(__('Need more info'), 
			cur_frm.cscript['Insufficient Info']);
	}
	if(frappe.user.has_role("CBDO") && frm.doc.status == "COO Approved")
	{
		cur_frm.add_custom_button(__('CBDO Approve'), 
			cur_frm.cscript['CBDO Approval']);
		cur_frm.add_custom_button(__('Need more info'), 
			cur_frm.cscript['Insufficient Info']);
	}
	if(frm.doc.status == "Insufficient Information")
	{
		cur_frm.call({
			doc: cur_frm.doc,
			method: "insufficient_info_remark",
			callback: function(r) {
				if(r.exc) {
					msgprint(__("There were errors."));
				} else {
					console.log("success");
					console.log(r.message);
					cur_frm.set_intro(__(r.message));
				}
			}
		});
	}
	
	
	if((frm.doc.status==="Rfq" || frm.doc.status==="RFQ")  && (frm.doc.prev_status==="Rfq" || frm.doc.prev_status==="RFQ") && !(frappe.user.has_role("Sales Master Manager")))
	{
		//cur_frm.timeline.insert_comment("Workflow", "Information Added");
		cur_frm.add_custom_button(__('Information Added'), 
			cur_frm.cscript['Send for Approval']);
		
	}
	if(frm.doc.status==="KAM Approved" && frm.doc.prev_status==="KAM Approved"  && !(frappe.user.has_role("Sales Master Manager")))
	{
		//cur_frm.timeline.insert_comment("Workflow", "Information Added");
		cur_frm.add_custom_button(__('Information Added'), 
			cur_frm.cscript['Send for Approval']);
	}
	if(frm.doc.status==="COO Approved" && frm.doc.prev_status==="COO Approved"  && !(frappe.user.has_role("Sales Master Manager")))
	{
		//cur_frm.timeline.insert_comment("Workflow", "Information Added");
		cur_frm.add_custom_button(__('Information Added'), 
			cur_frm.cscript['Send for Approval']);
	}
	if(frm.doc.status==="RFQ Approved" && frm.doc.prev_status==="RFQ Approved"  && !(frappe.user.has_role("Sales Master Manager")))
	{
		//cur_frm.timeline.insert_comment("Workflow", "Information Added");
		cur_frm.add_custom_button(__('Information Added'), 
			cur_frm.cscript['Notify D&E']);
	}
	if(frm.doc.status==="RFQ Approved" || frm.doc.status==="Boq" || frm.doc.status==="BOQ" || frm.doc.status==="Quotation" && !(frappe.user.has_role("Sales Manager")))
	{
		cur_frm.add_custom_button(__("Close"), function() {
				frm.set_value("status", "Closed");
				frm.save();
			});
	}
	
	
	
	// new addition
	
	
	if(frm.perm[0].write && doc.docstatus==0 && !((frappe.user.has_role("Security") || frappe.user.has_role("AV") || frappe.user.has_role("BMS") || frappe.user.has_role("Business Automation"))) && !(frappe.user.has_role("Sales Master Manager"))) 
	{
		if(frm.doc.status==="Open") {
			cur_frm.add_custom_button(__("Close"), function() {
				frm.set_value("status", "Closed");
				frm.save();
			});
		} else {
			cur_frm.add_custom_button(__("Reopen"), 
			cur_frm.cscript['Reopen']);
		}
	}

	if(doc.status!=="Lost" && !((frappe.user.has_role("Security") || frappe.user.has_role("AV") || frappe.user.has_role("BMS") || frappe.user.has_role("Business Automation"))) && !(frappe.user.has_role("Sales Master Manager"))) {
		if(doc.status!=="Quotation") {
			cur_frm.add_custom_button(__('Lost'),
				cur_frm.cscript['Declare Opportunity Lost']);
		}

		//cur_frm.add_custom_button(__('Quotation'),
		//	cur_frm.cscript.create_quotation);
	}
	
	

	cur_frm.add_custom_button(__('Refresh'),
			cur_frm.cscript['Refresh']);
	

}

cur_frm.cscript.onload_post_render = function(doc, cdt, cdn) {
	if(doc.enquiry_from == 'Lead' && doc.lead)
		cur_frm.cscript.lead(doc, cdt, cdn);
}

cur_frm.cscript.item_code = function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	if (d.item_code) {
		return frappe.call({
			method: "erpnext.crm.doctype.opportunity.opportunity.get_item_details",
			args: {"item_code":d.item_code},
			callback: function(r, rt) {
				if(r.message) {
					$.each(r.message, function(k, v) {
						frappe.model.set_value(cdt, cdn, k, v);
					});
				refresh_field('image_view', d.name, 'items');
				}
			}
		})
	}
}

cur_frm.cscript.lead = function(doc, cdt, cdn) {
	cur_frm.toggle_display("contact_info", doc.customer || doc.lead);
	erpnext.utils.map_current_doc({
		method: "erpnext.crm.doctype.lead.lead.make_opportunity",
		source_name: cur_frm.doc.lead,
		frm: cur_frm
	});
}

cur_frm.cscript['Declare Opportunity Lost'] = function() {
	var dialog = new frappe.ui.Dialog({
		title: __("Set as Lost"),
		fields: [
			{"fieldtype": "Text", "label": __("Reason for losing"), "fieldname": "reason",
				"reqd": 1 },
			{"fieldtype": "Button", "label": __("Update"), "fieldname": "update"},
		]
	});

	dialog.fields_dict.update.$input.click(function() {
		args = dialog.get_values();
		if(!args) return;
		return cur_frm.call({
			doc: cur_frm.doc,
			method: "declare_enquiry_lost",
			args: args.reason,
			callback: function(r) {
				if(r.exc) {
					msgprint(__("There were errors."));
				} else {
					dialog.hide();
					cur_frm.refresh();
				}
			},
			btn: this
		})
	});
	dialog.show();
}



//new addition

cur_frm.cscript['Send for Approval'] = function(){
	if(cur_frm.doc.status == cur_frm.doc.prev_status)
	{	
		cur_frm.timeline.insert_comment("Workflow", "Information Added");
	}
	//alert("what is this!!!")
	cur_frm.call({
			doc: cur_frm.doc,
			method: "send_notification",
			args: "need_approval",
			callback: function(r) {
				if(r.exc) {
					msgprint(__("There were errors."));
				} else {
					//cur_frm.timeline.insert_comment("Workflow", "Sent for Approval");
					msgprint(__("Succesfully Send for Approval !!!!!"));
					location.reload();
				}
			}
		});
	
}

cur_frm.cscript['Insufficient Info'] = function(){
	var dialog = new frappe.ui.Dialog({
		title: "Need more info",
		fields: [
			{"fieldtype": "Text", "label": __("Remarks"), "fieldname": "reason",
				"reqd": 1 },
			{"fieldtype": "Button", "label": __("Update"), "fieldname": "update"},
		]
		
	});
	dialog.show();
	dialog.fields_dict.update.$input.click(function() {
		args = dialog.get_values();
		if(!args) return;
		cur_frm.set_value("prev_status", cur_frm.doc.status)
		cur_frm.set_value("status", "Insufficient Information");
		cur_frm.set_value("to_discuss", args.reason);
		cur_frm.set_intro(__(args.reason));
		cur_frm.timeline.insert_comment("Workflow", "Insufficient Information Reason: " + args.reason);
		cur_frm.save();
		dialog.hide();
			
		return cur_frm.call({
			doc: cur_frm.doc,
			method: "send_notification",
			args:"need_info",
			callback: function(r) {
				if(r.exc) {
					dialog.hide();
					msgprint(__("There were errors."));
				} else {
					dialog.hide();
					//msgprint(__("Succesfully Send for Approval !!!!!"));
					//location.reload();
				}
			}
		});
		
		
	});
	
}

cur_frm.cscript['COO Approval'] = function()
{
		cur_frm.call({
			doc: cur_frm.doc,
			method: "approval",
			args: "COO",
			callback: function(r) {
				if(r.exc) {
					msgprint(__("There were errors."));
				} else {
					msgprint(__("Successfully Approved !!!!!"));
					cur_frm.timeline.insert_comment("Workflow", "Approved");
					location.reload();
				}
			}
		});
}


cur_frm.cscript['CBDO Approval'] = function()
{
		cur_frm.call({
			doc: cur_frm.doc,
			method: "approval",
			args: "CBDO",
			callback: function(r) {
				if(r.exc) {
					msgprint(__("There were errors."));
				} else {
					msgprint(__("Successfully Approved !!!!!"));
					cur_frm.timeline.insert_comment("Workflow", "Approved");
					location.reload();
				}
			}
		});
}


cur_frm.cscript['SAM Approval'] = function()
{
		
		cur_frm.call({
			doc: cur_frm.doc,
			method: "approval",
			args: "SAM",
			callback: function(r) {
				if(r.exc) {
					msgprint(__("There were errors."));
				} else {
					msgprint(__("Successfully Approved !!!!!"));
					cur_frm.timeline.insert_comment("Workflow", "Approved");
					location.reload();
				}
			}
		});	
}



cur_frm.cscript['Reopen'] = function()
{
	cur_frm.call({
			doc: cur_frm.doc,
			method: "reopen",
			callback: function(r) {
				if(r.exc) {
					msgprint(__("There were errors."));
				} else {
					msgprint(__("Reopened successfully to last state. Kindly save the data!!!!!"));
					cur_frm.set_value("status", r.message);
					cur_frm.timeline.insert_comment("Workflow", "Reopened");
				}
			}
		});	
	
}

cur_frm.cscript['Notify D&E'] = function()
{
	cur_frm.timeline.insert_comment("Workflow", "Information Added");
	cur_frm.call({
			doc: cur_frm.doc,
			method: "send_notification",
			args:"added_info",
			callback: function(r) {
				if(r.exc) {
					msgprint(__("There were errors."));
				} else {
					msgprint(__("Notified Design & Estimation Team !!!!!"));
					cur_frm.timeline.insert_comment("Workflow", "Information Added & Notified to D&E Team");
					location.reload();
				}
			}
		});
	
}

cur_frm.cscript['Refresh']= function(){
	location.reload();
}
//new addition
