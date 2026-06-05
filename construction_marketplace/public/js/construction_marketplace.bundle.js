// Copyright (c) 2024, Sudhakar and contributors
// For license information, please see license.txt

// Construction Marketplace JS Bundle

frappe.provide("construction_marketplace");

frappe.pages["construction-marketplace-dashboard"].onload = function(wrapper) {
    frappe.call({
        method: "construction_marketplace.construction_marketplace.utils.get_dashboard_data",
        callback: function(r) {
            if (r.message) {
                // Render dashboard with data
            }
        }
    });
};

frappe.form.formatters["Material Category"] = function(value, doc, fieldname) {
    if (value) {
        return `<span class="cm-category-badge">${value}</span>`;
    }
    return value;
};

$(document).on("form-render", function(e, wrapper) {
    if (wrapper.data && wrapper.data.doctype === "Marketplace Order") {
        var status = wrapper.data.status;
        if (status) {
            wrapper.$wrapper.find(".page-title")
                .addClass("order-status-" + status.toLowerCase());
        }
    }
});
