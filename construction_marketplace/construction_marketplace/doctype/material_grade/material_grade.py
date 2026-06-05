# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class MaterialGrade(Document):
    """Material Grade document - e.g., OPC 43, OPC 53, Fe 500, Fe 500D"""
    
    def validate(self):
        if not self.grade_name:
            frappe.throw("Grade name is required")
