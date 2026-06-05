// Copyright (c) 2024, Sudhakar and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Analysis Report"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "width": 80
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "width": 80
        },
        {
            "fieldname": "status",
            "label": __("Order Status"),
            "fieldtype": "Select",
            "options": [
                "",
                "Draft",
                "Confirmed",
                "Processing",
                "Shipped",
                "Delivered",
                "Cancelled"
            ],
            "width": 100
        },
        {
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Marketplace Customer",
            "width": 100
        }
    ]
};
