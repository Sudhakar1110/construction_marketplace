# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    
    columns = get_columns()
    data = get_data(filters)
    
    return columns, data


def get_columns():
    return [
        {
            "fieldname": "supplier",
            "label": _("Supplier"),
            "fieldtype": "Link",
            "options": "Supplier",
            "width": 150
        },
        {
            "fieldname": "supplier_name",
            "label": _("Supplier Name"),
            "fieldtype": "Data",
            "width": 180
        },
        {
            "fieldname": "total_materials",
            "label": _("Materials Supplied"),
            "fieldtype": "Int",
            "width": 130
        },
        {
            "fieldname": "total_orders",
            "label": _("Total Orders"),
            "fieldtype": "Int",
            "width": 110
        },
        {
            "fieldname": "delivered_orders",
            "label": _("Delivered Orders"),
            "fieldtype": "Int",
            "width": 130
        },
        {
            "fieldname": "delivery_rate",
            "label": _("Delivery Rate (%)"),
            "fieldtype": "Percent",
            "width": 120
        },
        {
            "fieldname": "avg_rating",
            "label": _("Avg Rating"),
            "fieldtype": "Float",
            "width": 100
        },
        {
            "fieldname": "quality_passes",
            "label": _("Quality Passes"),
            "fieldtype": "Int",
            "width": 110
        },
        {
            "fieldname": "quality_fails",
            "label": _("Quality Fails"),
            "fieldtype": "Int",
            "width": 100
        }
    ]


def get_data(filters):
    conditions = ""
    
    if filters and filters.get("supplier"):
        conditions = f"AND s.name = '{filters.get('supplier')}'"
    elif filters and filters.get("min_rating"):
        conditions = f"AND (s.rating >= {filters.get('min_rating')} OR s.rating IS NULL)"
    
    query = f"""
        SELECT
            s.name as supplier,
            s.supplier_name,
            s.rating as avg_rating,
            COALESCE(material_count.total, 0) as total_materials,
            COALESCE(order_count.total, 0) as total_orders,
            COALESCE(delivered_count.total, 0) as delivered_orders,
            CASE 
                WHEN COALESCE(order_count.total, 0) > 0 
                THEN ROUND((COALESCE(delivered_count.total, 0) * 100.0 / order_count.total), 1)
                ELSE 0 
            END as delivery_rate,
            COALESCE(qc_pass.total, 0) as quality_passes,
            COALESCE(qc_fail.total, 0) as quality_fails
        FROM
            `tabSupplier` s
        LEFT JOIN (
            SELECT supplier, COUNT(*) as total
            FROM `tabMaterial Price`
            WHERE docstatus < 2
            GROUP BY supplier
        ) material_count ON s.name = material_count.supplier
        LEFT JOIN (
            SELECT supplier, COUNT(*) as total
            FROM `tabQuality Check`
            WHERE docstatus < 2
            GROUP BY supplier
        ) qc_pass ON s.name = qc_pass.supplier
        LEFT JOIN (
            SELECT supplier, COUNT(*) as total
            FROM `tabQuality Check`
            WHERE docstatus < 2 AND result = 'Rejected'
            GROUP BY supplier
        ) qc_fail ON s.name = qc_fail.supplier
        LEFT JOIN (
            SELECT supplier, COUNT(DISTINCT mp.name) as total
            FROM `tabMarketplace Order` mp
            INNER JOIN `tabOrder Item` oi ON oi.parent = mp.name
            INNER JOIN `tabMaterial Price` mpr ON mpr.material = oi.item_code AND mpr.supplier = s.name
            WHERE mp.docstatus < 2
            GROUP BY supplier
        ) order_count ON 1=1
        LEFT JOIN (
            SELECT oi.item_code, COUNT(DISTINCT mp.name) as total
            FROM `tabMarketplace Order` mp
            INNER JOIN `tabOrder Item` oi ON oi.parent = mp.name
            WHERE mp.status = 'Delivered' AND mp.docstatus < 2
            GROUP BY oi.item_code
        ) delivered_count ON 1=1
        WHERE
            s.docstatus < 2
            {conditions}
        ORDER BY
            delivery_rate DESC, s.supplier_name
    """
    
    return frappe.db.sql(query, as_dict=True)
