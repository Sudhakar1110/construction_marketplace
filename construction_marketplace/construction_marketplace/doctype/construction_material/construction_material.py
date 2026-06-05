# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _


class ConstructionMaterial(Document):
    """Construction Material document - Main product catalog Item"""
    
    def validate(self):
        self.validate_material_name()
    
    def validate_material_name(self):
        if not self.material_name:
            frappe.throw(_("Material name is required"))
    
    def before_save(self):
        self.set_title()
    
    def set_title(self):
        if self.material_name and self.material_grade:
            self.title = f"{self.material_name} - {self.material_grade}"
        elif self.material_name:
            self.title = self.material_name
        elif self.material_grade:
            grade = frappe.get_doc("Material Grade", self.material_grade)
            self.title = grade.grade_name
