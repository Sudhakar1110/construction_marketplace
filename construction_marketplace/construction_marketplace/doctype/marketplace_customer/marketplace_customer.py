# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _


class MarketplaceCustomer(Document):
    """Marketplace Customer/Buyer document"""
    
    def validate(self):
        self.validate_contact()
    
    def validate_contact(self):
        if not self.email and not self.phone and not self.mobile:
            frappe.msgprint(_("Please provide at least one contact method"), alert=True)
    
    def before_save(self):
        if self.customer_name:
            self.customer_name = self.customer_name.strip()
