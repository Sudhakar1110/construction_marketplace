# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class MaterialCategory(Document):
    """Material Category document - e.g., Cement, TMT Steel, M Sand, Bricks, Blocks"""
    
    def validate(self):
        if not self.title:
            frappe.throw("Category title is required")
    
    def before_save(self):
        if self.title:
            self.title = self.title.strip()
