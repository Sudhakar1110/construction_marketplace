# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import nowdate


class DeliverySchedule(Document):
    """Delivery Schedule - Track material shipments"""
    
    def validate(self):
        self.validate_dates()
    
    def validate_dates(self):
        if self.scheduled_date and self.scheduled_date < nowdate():
            frappe.msgprint(_("Scheduled date is in the past"), alert=True)
    
    def before_save(self):
        if self.delivery_status == "Delivered" and not self.actual_delivery_date:
            self.actual_delivery_date = nowdate()
    
    def on_submit(self):
        self.update_order_delivery_status()
    
    def update_order_delivery_status(self):
        if self.order:
            order = frappe.get_doc("Marketplace Order", self.order)
            all_delivered = True
            any_delivered = False
            
            for item in order.items:
                if item.delivery_status == "Delivered":
                    any_delivered = True
                elif item.delivery_status in ["Pending", "Partially Delivered"]:
                    all_delivered = False
            
            if all_delivered and any_delivered:
                order.status = "Delivered"
            elif any_delivered:
                order.status = "Shipped"
            
            order.flags.ignore_permissions = True
            order.save()
