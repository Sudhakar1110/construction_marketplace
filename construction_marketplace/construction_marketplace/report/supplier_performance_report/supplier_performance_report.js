// Copyright (c) 2024, Sudhakar and contributors
// For license information, please see license.txt

frappe.query_reports["Supplier Performance Report"] = {
    "filters": [
        {
            "fieldname": "supplier",
            "label": __("Supplier"),
            "fieldtype": "Link",
            "options": "Supplier",
            "width": 100
        },
        {
            "fieldname": "min_rating",
            "label": __("Min Rating"),
            "fieldtype": "Float",
            "width": 80
        }
    ],
    "formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        
        if (column.fieldname === "delivery_rate") {
            if (data && data.delivery_rate < 50) {
                value = `<span class="text-danger">${value}</span>`;
            } else if (data && data.delivery_rate < 75) {
                value = `<span class="text-warning">${value}</span>`;
            } else if (data && data.delivery_rate >= 75) {
                value = `<span class="text-success">${value}</span>`;
            }
        }
        
        return value;
    }
};
