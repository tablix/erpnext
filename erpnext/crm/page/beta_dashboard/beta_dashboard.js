frappe.pages['beta_dashboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'None',
		single_column: true





	});

	this.page = wrapper.page;

	this.page.set_title(__("DashBoard"));
}
