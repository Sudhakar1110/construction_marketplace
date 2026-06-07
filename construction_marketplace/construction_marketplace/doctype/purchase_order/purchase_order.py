# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _


class PurchaseOrder(Document):
    """Purchase Order - Order sent to suppliers for procuring materials"""
    
    def validate(self):
        self.calculate_totals()
        self.validate_dates()
    
    def validate_dates(self):
        if self.expected_delivery_date and self.order_date:
            if self.expected_delivery_date < self.order_date:
                frappe.throw(_("Expected delivery date cannot be before order date"))
    
    def calculate_totals(self):
        total_qty = 0
        total_amount = 0
        
        for item in self.get("items", []):
            if item.qty and item.rate:
                item.amount = item.qty * item.rate
                total_qty += item.qty
                total_amount += item.amount
        
        self.total_qty = total_qty
        self.total_amount = total_amount
        self.net_amount = total_amount - (self.discount_amount or 0)
    
    def before_submit(self):
        if not self.get("items"):
            frappe.throw(_("At least one item is required to submit the purchase order"))
        if self.status == "Draft":
            self.status = "Submitted"
    
    def before_cancel(self):
        self.status = "Cancelled"
