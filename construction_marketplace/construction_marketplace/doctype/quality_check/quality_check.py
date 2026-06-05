# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _


class QualityCheck(Document):
    """Quality Check - Material quality inspection document"""
    
    def validate(self):
        self.calculate_results()
    
    def calculate_results(self):
        """Auto-calculate overall result based on parameters"""
        if self.get("parameters"):
            all_pass = True
            for param in self.parameters:
                if param.result != "Pass":
                    all_pass = False
                    break
            
            if all_pass:
                self.result = "Accepted"
            elif not self.quantity_rejected:
                self.result = "Accepted"
            elif self.quantity_rejected >= self.quantity_checked:
                self.result = "Rejected"
            else:
                self.result = "Conditional"
