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
        self.set_title()
    
    def validate_material_name(self):
        if not self.material_name:
            frappe.throw(_("Material name is required"))
    
    def before_save(self):
        self.set_route()
    
    def set_title(self):
        if self.material_name and self.material_grade:
            self.title = f"{self.material_name} - {self.material_grade}"
        elif self.material_name:
            self.title = self.material_name
        elif self.material_grade:
            grade = frappe.get_doc("Material Grade", self.material_grade)
            self.title = grade.grade_name
    
    def set_route(self):
        """Auto-generate a clean URL-friendly slug for this material"""
        if not self.route and self.material_name:
            import re
            base_slug = re.sub(r'[^a-zA-Z0-9]+', '-', self.material_name.lower()).strip('-')
            if not base_slug:
                base_slug = f"material-{frappe.generate_hash(length=6)}"
            # Ensure uniqueness — for new docs self.name is not yet set, so we exclude based on name being empty
            existing_name = self.name or ""
            existing = frappe.db.get_value("Construction Material", {"route": base_slug, "name": ["!=", existing_name]}, "name")
            if existing:
                base_slug = f"{base_slug}-{frappe.generate_hash(length=4)}"
            self.route = base_slug
