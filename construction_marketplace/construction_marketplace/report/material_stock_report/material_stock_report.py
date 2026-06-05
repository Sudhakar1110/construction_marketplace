# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    columns, data = [], []
    
    columns = get_columns()
    data = get_data(filters)
    
    return columns, data


def get_columns():
    return [
        {
            "fieldname": "material_name",
            "label": _("Material Name"),
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "category",
            "label": _("Category"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "grade",
            "label": _("Grade"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "brand",
            "label": _("Brand"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "unit_of_measure",
            "label": _("UOM"),
            "fieldtype": "Data",
            "width": 80
        },
        {
            "fieldname": "current_stock",
            "label": _("Current Stock"),
            "fieldtype": "Float",
            "width": 100
        },
        {
            "fieldname": "reorder_level",
            "label": _("Reorder Level"),
            "fieldtype": "Float",
            "width": 100
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "last_restock_date",
            "label": _("Last Restock"),
            "fieldtype": "Date",
            "width": 100
        }
    ]


def get_data(filters):
    conditions = []
    
    if filters and filters.get("category"):
        conditions.append(f"cm.material_category = '{filters.get('category')}'")
    
    if filters and filters.get("status"):
        if filters.get("status") == "Low Stock":
            conditions.append("(cm.current_stock <= cm.reorder_level OR (cm.reorder_level IS NULL AND cm.current_stock <= 10))")
        elif filters.get("status") == "In Stock":
            conditions.append("(cm.current_stock > cm.reorder_level OR cm.reorder_level IS NULL)")
        elif filters.get("status") == "Out of Stock":
            conditions.append("(cm.current_stock IS NULL OR cm.current_stock <= 0)")
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    query = f"""
        SELECT
            cm.name as material_id,
            cm.material_name,
            mc.title as category,
            mg.grade_name as grade,
            cm.brand,
            cm.unit_of_measure,
            cm.current_stock,
            cm.reorder_level,
            cm.last_restock_date,
            CASE
                WHEN cm.current_stock IS NULL OR cm.current_stock <= 0 THEN 'Out of Stock'
                WHEN cm.reorder_level IS NOT NULL AND cm.current_stock <= cm.reorder_level THEN 'Low Stock'
                ELSE 'In Stock'
            END as status
        FROM
            `tabConstruction Material` cm
        LEFT JOIN
            `tabMaterial Category` mc ON cm.material_category = mc.name
        LEFT JOIN
            `tabMaterial Grade` mg ON cm.material_grade = mg.name
        WHERE
            cm.docstatus < 2
            AND {where_clause}
        ORDER BY
            cm.material_name
    """
    
    return frappe.db.sql(query, as_dict=True)
