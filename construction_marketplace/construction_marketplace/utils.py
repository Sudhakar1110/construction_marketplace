# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import today, nowdate, flt


@frappe.whitelist()
def get_dashboard_data():
    """Get dashboard statistics for Construction Marketplace"""
    data = {}
    
    data["total_materials"] = frappe.db.count("Construction Material", {"is_active": 1})
    data["total_categories"] = frappe.db.count("Material Category", {"is_active": 1})
    data["total_suppliers"] = frappe.db.count("Supplier")
    data["total_customers"] = frappe.db.count("Marketplace Customer")
    
    data["pending_orders"] = frappe.db.count("Marketplace Order", {"status": ["!=", "Delivered"], "status": ["!=", "Cancelled"]})
    data["open_enquiries"] = frappe.db.count("Customer Enquiry", {"status": "Open"})
    data["pending_deliveries"] = frappe.db.count("Delivery Schedule", {"delivery_status": ["!=", "Delivered"]})
    
    return data


@frappe.whitelist()
def get_material_categories():
    """Get active material categories for website"""
    categories = frappe.get_all(
        "Material Category",
        filters={"is_active": 1},
        fields=["name", "title", "description", "category_image"],
        order_by="title"
    )
    return categories


@frappe.whitelist()
def get_materials_by_category(category=None):
    """Get construction materials filtered by category"""
    filters = {"is_active": 1}
    
    if category:
        filters["material_category"] = category
    
    materials = frappe.get_all(
        "Construction Material",
        filters=filters,
        fields=["name", "material_name", "brand", "unit_of_measure",
                "image", "description", "material_category", "material_grade"],
        order_by="material_name"
    )
    
    return materials


@frappe.whitelist()
def get_material_price(material, supplier=None):
    """Get current price for a material"""
    filters = {
        "material": material,
        "is_active": 1,
        "effective_from": ["<=", today()],
        "effective_to": [">=", today()]
    }
    
    if supplier:
        filters["supplier"] = supplier
    
    prices = frappe.get_all(
        "Material Price",
        filters=filters,
        fields=["name", "supplier", "supplier_name", "price_per_unit",
                "unit_of_measure", "minimum_order_qty", "currency"],
        order_by="price_per_unit"
    )
    
    return prices


@frappe.whitelist()
def create_order_from_enquiry(enquiry_id):
    """Convert a customer enquiry into a marketplace order"""
    enquiry = frappe.get_doc("Customer Enquiry", enquiry_id)
    
    if enquiry.status != "Open":
        frappe.throw(_("Enquiry is not in Open status"))
    
    order = frappe.new_doc("Marketplace Order")
    order.customer = enquiry.customer
    order.order_date = today()
    order.delivery_date = enquiry.preferred_delivery_date
    order.delivery_address = enquiry.delivery_address
    
    if enquiry.material:
        order.append("items", {
            "item_code": enquiry.material,
            "quantity": enquiry.quantity or 1,
            "rate": 0
        })
    
    order.flags.ignore_permissions = True
    order.insert()
    
    enquiry.status = "Converted to Order"
    enquiry.flags.ignore_permissions = True
    enquiry.save()
    
    return order.name
