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
            "fieldname": "order_id",
            "label": _("Order ID"),
            "fieldtype": "Link",
            "options": "Marketplace Order",
            "width": 140
        },
        {
            "fieldname": "order_date",
            "label": _("Order Date"),
            "fieldtype": "Date",
            "width": 100
        },
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "customer_type",
            "label": _("Customer Type"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "item_count",
            "label": _("Items"),
            "fieldtype": "Int",
            "width": 60
        },
        {
            "fieldname": "total_amount",
            "label": _("Total Amount"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "discount_amount",
            "label": _("Discount"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "net_amount",
            "label": _("Net Amount"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "payment_status",
            "label": _("Payment Status"),
            "fieldtype": "Data",
            "width": 110
        }
    ]


def get_data(filters):
    conditions = []
    
    if filters:
        if filters.get("from_date"):
            conditions.append(f"mo.order_date >= '{filters.get('from_date')}'")
        if filters.get("to_date"):
            conditions.append(f"mo.order_date <= '{filters.get('to_date')}'")
        if filters.get("status"):
            conditions.append(f"mo.status = '{filters.get('status')}'")
        if filters.get("customer"):
            conditions.append(f"mo.customer = '{filters.get('customer')}'")
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    query = f"""
        SELECT
            mo.name as order_id,
            mo.order_date,
            mo.customer_name as customer,
            mc.customer_type,
            (SELECT COUNT(*) FROM `tabOrder Item` oi WHERE oi.parent = mo.name) as item_count,
            mo.total_amount,
            mo.discount_amount,
            mo.net_amount,
            mo.status,
            mo.payment_status
        FROM
            `tabMarketplace Order` mo
        LEFT JOIN
            `tabMarketplace Customer` mc ON mo.customer = mc.name
        WHERE
            mo.docstatus < 2
            AND {where_clause}
        ORDER BY
            mo.order_date DESC, mo.creation DESC
    """
    
    return frappe.db.sql(query, as_dict=True)
