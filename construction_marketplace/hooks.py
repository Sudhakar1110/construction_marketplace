# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from . import __version__ as app_version

app_name = "construction_marketplace"
app_title = "Construction Marketplace"
app_publisher = "Sudhakar"
app_description = "A comprehensive Construction Materials Marketplace application for Frappe/ERPNext v15+"
app_email = ""
app_icon = "octicon octicon-git-branch"
app_color = "orange"
app_logo_url = "/assets/construction_marketplace/images/logo.png"
app_url = "https://github.com/Sudhakar1110/construction_marketplace"

# Apps
app_include_js = [
    "construction_marketplace.bundle.js"
]
app_include_css = [
    "construction_marketplace.bundle.css"
]

# Website
website_context = {
    "favicon": "/assets/construction_marketplace/images/favicon.png",
    "splash_image": "/assets/construction_marketplace/images/splash.png"
}

# DocType Class
# -----------------
doc_events = {}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "construction_marketplace.construction_marketplace.tasks.send_low_stock_alerts"
    ],
    "daily_long": [
        "construction_marketplace.construction_marketplace.tasks.update_order_statuses"
    ]
}

# Fixtures
# ---------
fixtures = [
    {"dt": "Role", "filters": [["name", "in", ["Construction Manager", "Supplier", "Customer"]]]},
    {"dt": "Workflow"},
    {"dt": "Workflow State"},
    {"dt": "Workflow Action"},
    {"dt": "Custom Field"},
]

# Permissions
# -----------
permission_query_conditions = {
    "Marketplace Order": "construction_marketplace.construction_marketplace.doctype.marketplace_order.marketplace_order.get_permission_query_conditions",
    "Customer Enquiry": "construction_marketplace.construction_marketplace.doctype.customer_enquiry.customer_enquiry.get_permission_query_conditions",
}

has_permission = {
    "Marketplace Order": "construction_marketplace.construction_marketplace.doctype.marketplace_order.marketplace_order.has_permission",
    "Customer Enquiry": "construction_marketplace.construction_marketplace.doctype.customer_enquiry.customer_enquiry.has_permission",
}

# Roles
# ------
after_install = "construction_marketplace.install.after_install"

# Website
# -------
# (disabled until configured as website generator)
