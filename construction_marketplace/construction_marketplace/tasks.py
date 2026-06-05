# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import today


def send_low_stock_alerts():
    """Daily task: Send notifications for low stock materials"""
    materials = frappe.get_all(
        "Construction Material",
        filters={
            "is_active": 1
        },
        fields=["name", "material_name", "current_stock", "reorder_level"]
    )
    
    low_stock_materials = []
    
    for mat in materials:
        reorder_level = mat.reorder_level or 0
        current_stock = mat.current_stock or 0
        
        if reorder_level > 0 and current_stock <= reorder_level:
            low_stock_materials.append(mat)
        elif reorder_level == 0 and current_stock <= 10:
            low_stock_materials.append(mat)
    
    if low_stock_materials:
        frappe.log_error(
            f"Low Stock Alert: {len(low_stock_materials)} materials are running low on stock.",
            "Construction Marketplace - Low Stock Alert"
        )
        
        for mat in low_stock_materials:
            subject = _("Low Stock Alert: {0}").format(mat.material_name)
            message = _("""
                <h3>Low Stock Alert</h3>
                <p><b>Material:</b> {0}</p>
                <p><b>Current Stock:</b> {1}</p>
                <p><b>Reorder Level:</b> {2}</p>
            """).format(mat.material_name, mat.current_stock, mat.reorder_level)
            
            # Get all users with Construction Manager role
            managers = frappe.db.get_all(
                "Has Role",
                filters={"role": "Construction Manager", "parenttype": "User"},
                pluck="parent"
            )
            if managers:
                manager_emails = []
                for manager in managers:
                    email = frappe.db.get_value("User", manager, "email")
                    if email:
                        manager_emails.append(email)
                
                if manager_emails:
                    frappe.sendmail(
                        recipients=manager_emails,
                        subject=subject,
                        message=message
                    )
    
    return len(low_stock_materials)


def update_order_statuses():
    """Daily long task: Update overdue order statuses"""
    # Mark orders as overdue if past delivery date
    overdue_orders = frappe.get_all(
        "Marketplace Order",
        filters={
            "status": ["in", ["Confirmed", "Processing", "Shipped"]],
            "delivery_date": ["<", today()],
            "docstatus": 1
        },
        fields=["name", "customer_name", "delivery_date"]
    )
    
    if overdue_orders:
        frappe.log_error(
            f"Overdue Orders: {len(overdue_orders)} orders are past their delivery date.",
            "Construction Marketplace - Overdue Orders"
        )


def check_low_stock(doc, method=None):
    """Check if stock is low and create notification"""
    if hasattr(doc, "current_stock") and hasattr(doc, "reorder_level"):
        reorder_level = doc.reorder_level or 0
        current_stock = doc.current_stock or 0
        
        if reorder_level > 0 and current_stock <= reorder_level:
            frappe.publish_realtime(
                "construction_marketplace_low_stock",
                {
                    "material": doc.name,
                    "material_name": doc.material_name,
                    "current_stock": current_stock,
                    "reorder_level": reorder_level
                },
                user=frappe.session.user
            )
