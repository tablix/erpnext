// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.projects");

cur_frm.add_fetch("project", "company", "company");

frappe.ui.form.on("Task", {
<<<<<<< HEAD
	onload: function(frm) {
		frm.set_query("task", "depends_on", function() {
			var filters = {
				name: ["!=", frm.doc.name]
			};
			if(frm.doc.project) filters["project"] = frm.doc.project;
			return {
				filters: filters
			};
		})
	},

	refresh: function(frm) {
		var doc = frm.doc;
		if(doc.__islocal) {
			if(!frm.doc.exp_end_date) {
				frm.set_value("exp_end_date", frappe.datetime.add_days(new Date(), 7));
			}
		}

=======
	refresh: function(frm) {
		var doc = frm.doc;
		//new addition
		frm.set_df_property("exp_start_date", "read_only", frm.doc.__islocal ? 0 : 1);
		frm.set_df_property("exp_end_date", "read_only", frm.doc.__islocal ? 0 : 1);
		if(doc.__islocal) {
			if(!frm.doc.exp_end_date) {
				frm.set_value("exp_start_date", frappe.datetime.add_days(new Date(), 0));
				frm.set_value("exp_end_date", frappe.datetime.add_days(new Date(), 7));
			}
		}
		
		//frm.toggle_display("project", frappe.user.has_role("Projects Users, Projects Manager"));
		
		if(inList(user_roles, "Projects User") || inList(user_roles, "Projects Manager"))
		{
			console.log("++")
			frm.toggle_display("project", true);
		}
		else
		{
			console.log("--")
			frm.toggle_display("project", false);
		}
		
		//new addition
		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		if(!doc.__islocal) {
			if(frappe.model.can_read("Timesheet")) {
				frm.add_custom_button(__("Timesheet"), function() {
					frappe.route_options = {"project": doc.project, "task": doc.name}
					frappe.set_route("List", "Timesheet");
				}, __("View"), true);
			}
			if(frappe.model.can_read("Expense Claim")) {
				frm.add_custom_button(__("Expense Claims"), function() {
<<<<<<< HEAD
					frappe.route_options = {"project": doc.project, "task": doc.name}
=======
					frappe.route_options = {"project": doc.project, "task": doc.name}	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
					frappe.set_route("List", "Expense Claim");
				}, __("View"), true);
			}

			if(frm.perm[0].write) {
				if(frm.doc.status!=="Closed" && frm.doc.status!=="Cancelled") {
					frm.add_custom_button(__("Close"), function() {
						frm.set_value("status", "Closed");
						frm.save();
<<<<<<< HEAD
=======
						frappe.call
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
					});
				} else {
					frm.add_custom_button(__("Reopen"), function() {
						frm.set_value("status", "Open");
						frm.save();
					});
				}
			}
		}
	},

	setup: function(frm) {
		frm.fields_dict.project.get_query = function() {
			return {
				query: "erpnext.projects.doctype.task.task.get_project"
			}
		};
	},

	project: function(frm) {
		if(frm.doc.project) {
			return get_server_fields('get_project_details', '','', frm.doc, frm.doc.doctype,
				frm.doc.name, 1);
		}
	},

	validate: function(frm) {
		frm.doc.project && frappe.model.remove_from_locals("Project",
			frm.doc.project);
	},

});

cur_frm.add_fetch('task', 'subject', 'subject');
<<<<<<< HEAD
cur_frm.add_fetch('task', 'project', 'project');
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
