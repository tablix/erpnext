// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["Minutes to First Response for Opportunity"] = {
<<<<<<< HEAD
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			'reqd': 1,
			"default": frappe.datetime.add_days(frappe.datetime.nowdate(), -30)
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			'reqd': 1,
			"default": frappe.datetime.nowdate()
		},
	],
	get_chart_data: function (columns, result) {
=======
    "filters": [
        {
            "fieldname":"from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
			'reqd': 1,
            "default": frappe.datetime.add_days(frappe.datetime.nowdate(), -30)
        },
        {
            "fieldname":"to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
			'reqd': 1,
            "default":frappe.datetime.nowdate()
        },
    ],
	get_chart_data: function(columns, result) {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		return {
			data: {
				x: 'Date',
				columns: [
<<<<<<< HEAD
					['Date'].concat($.map(result, function (d) { return d[0]; })),
					['Mins to first response'].concat($.map(result, function (d) { return d[1]; }))
				]
				// rows: [['Date', 'Mins to first response']].concat(result)
			},
			axis: {
				x: {
					type: 'timeseries',
					tick: {
						format: frappe.ui.py_date_format
					}
				}
			},
=======
					['Date'].concat($.map(result, function(d) { return d[0]; })),
					['Mins to first response'].concat($.map(result, function(d) { return d[1]; }))
				]
				// rows: [['Date', 'Mins to first response']].concat(result)
			},
		    axis: {
		        x: {
		            type: 'timeseries',
		            tick: {
		                format: frappe.ui.py_date_format
		            }
		        }
		    },
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			chart_type: 'line',

		}
	}
}
