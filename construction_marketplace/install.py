# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def after_install():
    """Run after app installation to set up default data"""
    create_default_roles()
    create_default_categories()
    create_default_grades()
    # Demo materials can be created after installation via:
    # bench --site your-site execute construction_marketplace.install.create_demo_materials


def create_default_roles():
    """Create default roles for the marketplace"""
    roles = [
        {
            "role_name": "Construction Manager",
            "desk_access": 1,
            "home_page": "/app/construction-marketplace"
        },
        {
            "role_name": "Supplier",
            "desk_access": 1,
            "home_page": "/app/construction-marketplace"
        },
        {
            "role_name": "Customer",
            "desk_access": 1,
            "home_page": "/app/construction-marketplace"
        }
    ]
    
    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.get_doc({
                "doctype": "Role",
                "role_name": role_data["role_name"],
                "desk_access": role_data["desk_access"],
                "home_page": role_data["home_page"]
            })
            role.insert(ignore_permissions=True)
    
    frappe.db.commit()


def create_default_categories():
    """Create default material categories"""
    categories = [
        {"title": "Cement", "description": "Portland cement, OPC, PPC and special cement varieties"},
        {"title": "TMT Steel", "description": "Thermo-Mechanically Treated steel bars and rods"},
        {"title": "M Sand", "description": "Manufactured sand for plastering and concrete work"},
        {"title": "Bricks", "description": "Red bricks, wirecut bricks and table mould bricks"},
        {"title": "Blocks", "description": "Solid concrete blocks and AAC lightweight blocks"},
        {"title": "Jelly Stones", "description": "Crushed stone aggregates for concrete mixing"},
        {"title": "Other Materials", "description": "Other construction materials and supplies"}
    ]
    
    for cat in categories:
        if not frappe.db.exists("Material Category", cat["title"]):
            doc = frappe.get_doc({
                "doctype": "Material Category",
                "title": cat["title"],
                "description": cat["description"],
                "is_active": 1
            })
            doc.insert(ignore_permissions=True)
    
    frappe.db.commit()


def create_default_grades():
    """Create default material grades"""
    grades = {
        "Cement": [
            {"grade_name": "OPC 43 Grade", "description": "Ordinary Portland Cement - 43 Grade"},
            {"grade_name": "OPC 53 Grade", "description": "Ordinary Portland Cement - 53 Grade"},
            {"grade_name": "PPC Grade", "description": "Pozzolana Portland Cement"},
            {"grade_name": "PSC Grade", "description": "Portland Slag Cement"}
        ],
        "TMT Steel": [
            {"grade_name": "Fe 500", "description": "Fe 500 Grade TMT Steel"},
            {"grade_name": "Fe 500D", "description": "Fe 500D Grade TMT Steel (Ductile)"},
            {"grade_name": "Fe 550", "description": "Fe 550 Grade TMT Steel"},
            {"grade_name": "Fe 550D", "description": "Fe 550D Grade TMT Steel"}
        ],
        "M Sand": [
            {"grade_name": "Plastering M Sand", "description": "Fine manufactured sand for plastering"},
            {"grade_name": "Concrete M Sand", "description": "Coarse manufactured sand for concrete"}
        ],
        "Bricks": [
            {"grade_name": "Red Bricks", "description": "Traditional clay red bricks"},
            {"grade_name": "Wirecut Bricks", "description": "Machine cut wirecut bricks"},
            {"grade_name": "Table Mould", "description": "Table mould bricks"}
        ],
        "Blocks": [
            {"grade_name": "Solid Concrete Blocks", "description": "Standard solid concrete blocks"},
            {"grade_name": "AAC Lightweight", "description": "Autoclaved Aerated Concrete blocks"}
        ]
    }
    
    for category_name, grade_list in grades.items():
        category = frappe.db.get_value("Material Category", {"title": category_name}, "name")
        if not category:
            continue
        
        for grade_data in grade_list:
            if not frappe.db.exists("Material Grade", grade_data["grade_name"]):
                doc = frappe.get_doc({
                    "doctype": "Material Grade",
                    "grade_name": grade_data["grade_name"],
                    "material_category": category,
                    "description": grade_data["description"],
                    "is_active": 1
                })
                doc.insert(ignore_permissions=True)
    
    frappe.db.commit()


def create_demo_materials():
    """Create demo construction materials"""
    materials = [
        {
            "material_name": "Ultratech PPC Cement",
            "category": "Cement",
            "grade": "PPC Grade",
            "brand": "Ultratech",
            "uom": "Bag",
            "reorder_level": 50
        },
        {
            "material_name": "ACC OPC 53 Grade Cement",
            "category": "Cement",
            "grade": "OPC 53 Grade",
            "brand": "ACC",
            "uom": "Bag",
            "reorder_level": 50
        },
        {
            "material_name": "JSW Fe 500D TMT Steel",
            "category": "TMT Steel",
            "grade": "Fe 500D",
            "brand": "JSW",
            "uom": "Ton",
            "reorder_level": 5
        },
        {
            "material_name": "Tata Tiscon Fe 500 TMT Steel",
            "category": "TMT Steel",
            "grade": "Fe 500",
            "brand": "Tata Tiscon",
            "uom": "Ton",
            "reorder_level": 5
        },
        {
            "material_name": "M Sand for Plastering",
            "category": "M Sand",
            "grade": "Plastering M Sand",
            "brand": "Premium",
            "uom": "Cubic Feet",
            "reorder_level": 100
        },
        {
            "material_name": "M Sand for Concrete",
            "category": "M Sand",
            "grade": "Concrete M Sand",
            "brand": "Premium",
            "uom": "Cubic Feet",
            "reorder_level": 100
        },
        {
            "material_name": "Wirecut Red Bricks",
            "category": "Bricks",
            "grade": "Wirecut Bricks",
            "brand": "Standard",
            "uom": "Pieces",
            "reorder_level": 1000
        },
        {
            "material_name": "AAC Lightweight Blocks",
            "category": "Blocks",
            "grade": "AAC Lightweight",
            "brand": "Buildmate",
            "uom": "Pieces",
            "reorder_level": 500
        }
    ]
    
    for mat in materials:
        category = frappe.db.get_value("Material Category", {"title": mat["category"]}, "name")
        grade = frappe.db.get_value("Material Grade", {"grade_name": mat["grade"]}, "name")
        
        if category and grade:
            title = f"{mat['material_name']} - {mat['grade']}"
            if not frappe.db.exists("Construction Material", {"title": title}):
                doc = frappe.get_doc({
                    "doctype": "Construction Material",
                    "material_name": mat["material_name"],
                    "title": title,
                    "material_category": category,
                    "material_grade": grade,
                    "brand": mat["brand"],
                    "unit_of_measure": mat["uom"],
                    "reorder_level": mat["reorder_level"],
                    "is_active": 1,
                    "current_stock": mat["reorder_level"] * 2
                })
                doc.insert(ignore_permissions=True)
    
    frappe.db.commit()
