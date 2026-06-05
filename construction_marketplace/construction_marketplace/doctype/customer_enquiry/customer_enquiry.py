# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _


class CustomerEnquiry(Document):
    """Customer Enquiry/Quote Request document"""
    
    def validate(self):
        self.validate_contact()
    
    def validate_contact(self):
        if not self.contact_number and not self.email:
            frappe.throw(_("Please provide at least contact number or email"))
    
    def on_update(self):
        if self.status == "Converted to Order" and not self.get("__islocal"):
            self.create_order_from_enquiry()
    
    def create_order_from_enquiry(self):
        if not self.material:
            return
        
        order = frappe.new_doc("Marketplace Order")
        order.customer = self.customer
        
        order.append("items", {
            "item_code": self.material,
            "quantity": self.quantity or 1,
            "rate": 0
        })
        
        order.flags.ignore_permissions = True
        order.insert()


def get_permission_query_conditions(user=None):
    """Permission conditions for Customer Enquiry"""
    if not user:
        user = frappe.session.user
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return None
    
    if "Construction Manager" in user_roles:
        return None
    
    return """(`tabCustomer Enquiry`.`owner` = {user})""".format(
        user=frappe.db.escape(user)
    )


def has_permission(doc, ptype, user):
    """Check if user has permission on this document"""
    if doc.owner == user:
        return True
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return True
    
    if "Construction Manager" in user_roles:
        return True
    
    return False
