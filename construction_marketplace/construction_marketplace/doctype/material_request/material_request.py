# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _


class MaterialRequest(Document):
    """Material Request - Internal request for procurement of materials"""
    
    def validate(self):
        self.validate_items()
        self.set_title()
    
    def set_title(self):
        """Auto-generate title from first item"""
        if not self.title and self.get("items"):
            first_item = self.items[0]
            if first_item.material_name:
                item_count = len(self.items)
                suffix = f" + {item_count - 1} more" if item_count > 1 else ""
                self.title = f"{first_item.material_name}{suffix}"
    
    def validate_items(self):
        if not self.get("items"):
            frappe.throw(_("At least one item is required"))
        
        for item in self.items:
            if item.qty and item.qty <= 0:
                frappe.throw(_("Quantity must be greater than zero"))
    
    def on_update(self):
        """Update status to Approved when status changes"""
        pass
    
    def before_submit(self):
        if self.status == "Draft":
            self.status = "Approved"
    
    def before_cancel(self):
        self.status = "Cancelled"
