frappe.ui.form.on("Issue", {
	"onload": function(frm) {
		frm.email_field = "raised_by";
	},
<<<<<<< HEAD

=======
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	"refresh": function(frm) {
		if(frm.doc.status==="Open") {
			frm.add_custom_button(__("Close"), function() {
				frm.set_value("status", "Closed");
				frm.save();
			});
		} else {
			frm.add_custom_button(__("Reopen"), function() {
<<<<<<< HEAD
=======
			//frm.set_df_property("date_time_closed", "default", "2017-01-01 00:00:01");
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				frm.set_value("status", "Open");
				frm.save();
			});
		}
<<<<<<< HEAD
	},

	timeline_refresh: function(frm) {
		// create button for "Help Article"
		if(frappe.model.can_create('Help Article')) {
			// Removing Help Article button if exists to avoid multiple occurance
			frm.timeline.wrapper.find('.comment-header .asset-details .btn-add-to-kb').remove();
			$('<button class="btn btn-xs btn-link btn-add-to-kb text-muted hidden-xs pull-right">'+
				__('Help Article') + '</button>')
				.appendTo(frm.timeline.wrapper.find('.comment-header .asset-details:not([data-communication-type="Comment"])'))
				.on('click', function() {
					var content = $(this).parents('.timeline-item:first').find('.timeline-item-content').html();
					var doc = frappe.model.get_new_doc('Help Article');
					doc.title = frm.doc.subject;
					doc.content = content;
					frappe.set_route('Form', 'Help Article', doc.name);
				});
		}
=======
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	}
});
