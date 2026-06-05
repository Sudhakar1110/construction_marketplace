# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from datetime import date


class MaterialPrice(Document):
    """Material Price - Pricing per material from suppliers"""
    
    def validate(self):
        self.validate_dates()
        self.validate_price()
    
    def validate_dates(self):
        if self.effective_from and self.effective_to:
            if self.effective_to < self.effective_from:
                frappe.throw(_("Effective To date cannot be before Effective From date"))
    
    def validate_price(self):
        if self.price_per_unit and self.price_per_unit <= 0:
            frappe.throw(_("Price per unit must be greater than zero"))
