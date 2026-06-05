// Copyright (c) 2024, Sudhakar and contributors
// For license information, please see license.txt

frappe.query_reports["Material Stock Report"] = {
    "filters": [
        {
            "fieldname": "category",
            "label": __("Material Category"),
            "fieldtype": "Link",
            "options": "Material Category",
            "width": 100
        },
        {
            "fieldname": "status",
            "label": __("Stock Status"),
            "fieldtype": "Select",
            "options": [
                "",
                "In Stock",
                "Low Stock",
                "Out of Stock"
            ],
            "width": 100
        }
    ],
    "formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        
        if (column.fieldname === "status") {
            if (data && data.status === "Out of Stock") {
                value = `<span class="text-danger">${value}</span>`;
            } else if (data && data.status === "Low Stock") {
                value = `<span class="text-warning">${value}</span>`;
            } else if (data && data.status === "In Stock") {
                value = `<span class="text-success">${value}</span>`;
            }
        }
        
        return value;
    }
};
