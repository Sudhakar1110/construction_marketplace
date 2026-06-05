# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _


class MarketplaceOrder(Document):
    """Marketplace Order - Main order document for construction materials"""
    
    def validate(self):
        self.calculate_totals()
        self.validate_dates()
    
    def validate_dates(self):
        if self.delivery_date and self.order_date:
            if self.delivery_date < self.order_date:
                frappe.throw(_("Delivery date cannot be before order date"))
    
    def calculate_totals(self):
        total = 0
        for item in self.get("items", []):
            if item.quantity and item.rate:
                item.amount = item.quantity * item.rate
                total += item.amount
        
        self.total_amount = total
        self.net_amount = total - (self.discount_amount or 0)
        self.balance_amount = self.net_amount - (self.advance_amount or 0)
    
    def before_submit(self):
        if not self.get("items"):
            frappe.throw(_("At least one item is required to submit the order"))
        if self.status not in ["Confirmed", "Processing"]:
            self.status = "Confirmed"
    
    def before_cancel(self):
        self.status = "Cancelled"


def get_permission_query_conditions(user=None):
    """Permission conditions for Marketplace Order"""
    if not user:
        user = frappe.session.user
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return None
    
    if "Construction Manager" in user_roles:
        return None
    
    if "Supplier" in user_roles:
        return None
    
    return """(`tabMarketplace Order`.`owner` = {user})""".format(
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
