frappe.ui.form.on("Course", "refresh", function(frm) {
	if(!cur_frm.doc.__islocal) {
		frm.add_custom_button(__("Program"), function() {
			frappe.route_options = {
				"Program Course.course": frm.doc.name
			}
			frappe.set_route("List", "Program");
		});
		
		frm.add_custom_button(__("Student Group"), function() {
			frappe.route_options = {
				course: frm.doc.name
			}
			frappe.set_route("List", "Student Group");
		});
		
		frm.add_custom_button(__("Course Schedule"), function() {
			frappe.route_options = {
				course: frm.doc.name
			}
			frappe.set_route("List", "Course Schedule");
		});
		
<<<<<<< HEAD
		frm.add_custom_button(__("Assessment Plan"), function() {
			frappe.route_options = {
				course: frm.doc.name
			}
			frappe.set_route("List", "Assessment Plan");
		});
	}

	frm.set_query('default_grading_scale', function(){
		return {
			filters: {
				docstatus: 1
			}
		}
	});
=======
		frm.add_custom_button(__("Assessment"), function() {
			frappe.route_options = {
				course: frm.doc.name
			}
			frappe.set_route("List", "Assessment");
		});
	}
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
});