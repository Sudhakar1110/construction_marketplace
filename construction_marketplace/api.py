# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, nowdate, add_days
import json


# ==================== MATERIAL APIS ====================

@frappe.whitelist(allow_guest=True)
def get_materials():
    """Get all active construction materials with pricing"""
    materials = frappe.db.sql("""
        SELECT
            cm.name as material_id,
            cm.material_name,
            cm.title,
            cm.brand,
            cm.unit_of_measure,
            cm.current_stock,
            cm.description,
            cm.image,
            cm.is_active,
            mc.title as category,
            mg.grade_name as grade,
            (SELECT MIN(mp.price_per_unit) FROM `tabMaterial Price` mp 
             WHERE mp.material = cm.name AND mp.is_active = 1 AND mp.docstatus < 2) as min_price,
            (SELECT COUNT(*) FROM `tabMaterial Price` mp 
             WHERE mp.material = cm.name AND mp.is_active = 1 AND mp.docstatus < 2) as supplier_count
        FROM
            `tabConstruction Material` cm
        LEFT JOIN
            `tabMaterial Category` mc ON cm.material_category = mc.name
        LEFT JOIN
            `tabMaterial Grade` mg ON cm.material_grade = mg.name
        WHERE
            cm.is_active = 1 AND cm.docstatus < 2
        ORDER BY
            cm.material_name ASC
    """, as_dict=True)
    
    return materials


@frappe.whitelist(allow_guest=True)
def get_material_details(material_id):
    """Get detailed information about a specific material"""
    if not material_id:
        frappe.throw(_("Material ID is required"))
    
    material = frappe.db.sql("""
        SELECT
            cm.*,
            mc.title as category,
            mc.description as category_description,
            mg.grade_name as grade,
            mg.description as grade_description
        FROM
            `tabConstruction Material` cm
        LEFT JOIN
            `tabMaterial Category` mc ON cm.material_category = mc.name
        LEFT JOIN
            `tabMaterial Grade` mg ON cm.material_grade = mg.name
        WHERE
            cm.name = %s AND cm.docstatus < 2
    """, material_id, as_dict=True)
    
    if not material:
        frappe.throw(_("Material not found"))
    
    material = material[0]
    
    # Get specifications
    material['specifications'] = frappe.db.sql("""
        SELECT specification, value
        FROM `tabMaterial Specification`
        WHERE parent = %s
        ORDER BY idx ASC
    """, material_id, as_dict=True)
    
    # Get pricing from suppliers
    material['prices'] = frappe.db.sql("""
        SELECT
            mp.name as price_id,
            mp.price_per_unit,
            mp.unit_of_measure,
            mp.minimum_order_qty,
            mp.currency,
            s.supplier_name,
            s.company_name,
            s.rating,
            s.city,
            s.is_approved,
            s.name as supplier_id
        FROM
            `tabMaterial Price` mp
        LEFT JOIN
            `tabSupplier` s ON mp.supplier = s.name
        WHERE
            mp.material = %s AND mp.is_active = 1 AND mp.docstatus < 2
        ORDER BY
            mp.price_per_unit ASC
    """, material_id, as_dict=True)
    
    # Stock status
    if material.current_stock and material.reorder_level:
        if material.current_stock <= 0:
            material['stock_status'] = 'out_of_stock'
        elif material.current_stock <= material.reorder_level:
            material['stock_status'] = 'low_stock'
        else:
            material['stock_status'] = 'in_stock'
    else:
        material['stock_status'] = 'in_stock' if (material.current_stock or 0) > 0 else 'unknown'
    
    return material


@frappe.whitelist(allow_guest=True)
def search_materials(query=None, category=None, min_price=None, max_price=None, supplier=None, page=1, page_size=12):
    """Search and filter materials with pagination"""
    conditions = ["cm.is_active = 1", "cm.docstatus < 2"]
    params = {}
    
    if query:
        safe_query = frappe.db.escape(f"%{query}%")
        conditions.append(f"(cm.material_name LIKE {safe_query} OR cm.brand LIKE {safe_query} OR cm.title LIKE {safe_query} OR mc.title LIKE {safe_query})")
    
    if category:
        safe_cat = frappe.db.escape(category)
        conditions.append(f"mc.title = {safe_cat}")
    
    price_join = ""
    price_conditions = ""
    if min_price or max_price or supplier:
        price_join = """
            INNER JOIN `tabMaterial Price` mp_filter ON mp_filter.material = cm.name
        """
        if min_price:
            price_conditions += f" AND mp_filter.price_per_unit >= {flt(min_price)}"
        if max_price:
            price_conditions += f" AND mp_filter.price_per_unit <= {flt(max_price)}"
        if supplier:
            safe_supplier = frappe.db.escape(supplier)
            price_conditions += f" AND mp_filter.supplier = {safe_supplier}"
        price_conditions += " AND mp_filter.is_active = 1 AND mp_filter.docstatus < 2"
    
    where_clause = " AND ".join(conditions)
    
    # Count total matching records
    count_query = f"""
        SELECT COUNT(DISTINCT cm.name) as total
        FROM `tabConstruction Material` cm
        LEFT JOIN `tabMaterial Category` mc ON cm.material_category = mc.name
        {price_join}
        WHERE {where_clause} {price_conditions}
    """
    total_count = frappe.db.sql(count_query, as_dict=True)[0].total
    
    # Pagination
    page = int(page)
    page_size = int(page_size)
    offset = (page - 1) * page_size
    
    data_query = f"""
        SELECT
            cm.name as material_id,
            cm.material_name,
            cm.title,
            cm.brand,
            cm.unit_of_measure,
            cm.current_stock,
            cm.image,
            cm.description,
            mc.title as category,
            mg.grade_name as grade,
            (SELECT MIN(mp.price_per_unit) FROM `tabMaterial Price` mp 
             WHERE mp.material = cm.name AND mp.is_active = 1 AND mp.docstatus < 2) as min_price,
            (SELECT COUNT(*) FROM `tabMaterial Price` mp 
             WHERE mp.material = cm.name AND mp.is_active = 1 AND mp.docstatus < 2) as supplier_count
        FROM
            `tabConstruction Material` cm
        LEFT JOIN
            `tabMaterial Category` mc ON cm.material_category = mc.name
        LEFT JOIN
            `tabMaterial Grade` mg ON cm.material_grade = mg.name
        {price_join}
        WHERE {where_clause} {price_conditions}
        GROUP BY cm.name
        ORDER BY cm.material_name ASC
        LIMIT {page_size} OFFSET {offset}
    """
    
    materials = frappe.db.sql(data_query, as_dict=True)
    
    return {
        "materials": materials,
        "total": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, -(-total_count // page_size))  # Ceiling division
    }


# ==================== CATEGORY APIS ====================

@frappe.whitelist(allow_guest=True)
def get_categories():
    """Get all active material categories with material count"""
    categories = frappe.db.sql("""
        SELECT
            mc.name,
            mc.title,
            mc.description,
            mc.category_image,
            (SELECT COUNT(*) FROM `tabConstruction Material` cm 
             WHERE cm.material_category = mc.name AND cm.is_active = 1 AND cm.docstatus < 2) as material_count
        FROM
            `tabMaterial Category` mc
        WHERE
            mc.is_active = 1 AND mc.docstatus < 2
        ORDER BY
            mc.title ASC
    """, as_dict=True)
    
    return categories


# ==================== SUPPLIER APIS ====================

@frappe.whitelist(allow_guest=True)
def get_suppliers():
    """Get all approved suppliers"""
    suppliers = frappe.db.sql("""
        SELECT
            s.name as supplier_id,
            s.supplier_name,
            s.company_name,
            s.contact_person,
            s.email,
            s.phone,
            s.mobile,
            s.website,
            s.rating,
            s.city,
            s.state,
            s.country,
            s.address as supplier_address,
            (SELECT COUNT(*) FROM `tabMaterial Price` mp 
             WHERE mp.supplier = s.name AND mp.is_active = 1 AND mp.docstatus < 2) as product_count
        FROM
            `tabSupplier` s
        WHERE
            s.is_approved = 1 AND s.docstatus < 2
        ORDER BY
            s.rating DESC, s.supplier_name ASC
    """, as_dict=True)
    
    return suppliers


@frappe.whitelist(allow_guest=True)
def get_supplier_products(supplier_id):
    """Get products from a specific supplier with pricing"""
    if not supplier_id:
        frappe.throw(_("Supplier ID is required"))
    
    products = frappe.db.sql("""
        SELECT
            mp.name as price_id,
            mp.price_per_unit,
            mp.unit_of_measure,
            mp.minimum_order_qty,
            mp.currency,
            mp.is_active,
            cm.name as material_id,
            cm.material_name,
            cm.brand,
            cm.image,
            cm.current_stock,
            mc.title as category
        FROM
            `tabMaterial Price` mp
        LEFT JOIN
            `tabConstruction Material` cm ON mp.material = cm.name
        LEFT JOIN
            `tabMaterial Category` mc ON cm.material_category = mc.name
        WHERE
            mp.supplier = %s AND mp.is_active = 1 AND mp.docstatus < 2
        ORDER BY
            cm.material_name ASC
    """, supplier_id, as_dict=True)
    
    return products


# ==================== CONTRACTOR APIS ====================

@frappe.whitelist(allow_guest=True)
def get_contractors(location=None, service=None, experience=None, page=1, page_size=12):
    """Get contractors from Marketplace Customers with type='Contractor'"""
    conditions = ["mc.customer_type = 'Contractor'", "mc.docstatus < 2"]
    
    if location:
        safe_location = frappe.db.escape(f"%{location}%")
        conditions.append(f"(mc.city LIKE {safe_location} OR mc.state LIKE {safe_location})")
    
    where_clause = " AND ".join(conditions)
    page = int(page)
    page_size = int(page_size)
    offset = (page - 1) * page_size
    
    total_count = frappe.db.sql(f"""
        SELECT COUNT(*) as total
        FROM `tabMarketplace Customer` mc
        WHERE {where_clause}
    """, as_dict=True)[0].total
    
    contractors = frappe.db.sql(f"""
        SELECT
            mc.name,
            mc.customer_name,
            mc.company_name,
            mc.contact_person,
            mc.email,
            mc.phone,
            mc.mobile,
            mc.city,
            mc.state,
            mc.is_verified,
            mc.notes as profile_description
        FROM
            `tabMarketplace Customer` mc
        WHERE {where_clause}
        ORDER BY mc.customer_name ASC
        LIMIT {page_size} OFFSET {offset}
    """, as_dict=True)
    
    return {
        "contractors": contractors,
        "total": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, -(-total_count // page_size))
    }


# ==================== ARCHITECT APIS ====================

@frappe.whitelist(allow_guest=True)
def get_architects(location=None, specialization=None, page=1, page_size=12):
    """Get architects from Marketplace Customers"""
    conditions = ["mc.customer_type = 'Architect'", "mc.docstatus < 2"]
    
    if location:
        safe_location = frappe.db.escape(f"%{location}%")
        conditions.append(f"(mc.city LIKE {safe_location} OR mc.state LIKE {safe_location})")
    
    where_clause = " AND ".join(conditions)
    page = int(page)
    page_size = int(page_size)
    offset = (page - 1) * page_size
    
    total_count = frappe.db.sql(f"""
        SELECT COUNT(*) as total
        FROM `tabMarketplace Customer` mc
        WHERE {where_clause}
    """, as_dict=True)[0].total
    
    architects = frappe.db.sql(f"""
        SELECT
            mc.name,
            mc.customer_name,
            mc.company_name,
            mc.contact_person,
            mc.email,
            mc.phone,
            mc.mobile,
            mc.city,
            mc.state,
            mc.is_verified,
            mc.notes as portfolio_description
        FROM
            `tabMarketplace Customer` mc
        WHERE {where_clause}
        ORDER BY mc.customer_name ASC
        LIMIT {page_size} OFFSET {offset}
    """, as_dict=True)
    
    return {
        "architects": architects,
        "total": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, -(-total_count // page_size))
    }


# ==================== CUSTOMER APIS ====================

@frappe.whitelist()
def get_customer_profile():
    """Get the current customer's profile"""
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Please login to access your profile"), frappe.PermissionError)
    
    # Try to find marketplace customer linked to this user
    customers = frappe.db.sql("""
        SELECT * FROM `tabMarketplace Customer`
        WHERE email = %s AND docstatus < 2
        LIMIT 1
    """, user, as_dict=True)
    customer = customers[0] if customers else None
    if not customer:
        # Also check by owner
        customers = frappe.db.sql("""
            SELECT * FROM `tabMarketplace Customer`
            WHERE owner = %s AND docstatus < 2
            LIMIT 1
        """, user, as_dict=True)
        customer = customers[0] if customers else None
    
    return customer


@frappe.whitelist()
def get_customer_orders(page=1, page_size=10):
    """Get orders for the current customer"""
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Please login first"), frappe.PermissionError)
    
    # Find the customer linked to this user
    customer = frappe.db.get_value("Marketplace Customer", {"email": user}, "name")
    if not customer:
        return {"orders": [], "total": 0}
    
    page = int(page)
    page_size = int(page_size)
    offset = (page - 1) * page_size
    
    total = frappe.db.count("Marketplace Order", {"customer": customer})
    
    orders = frappe.db.sql("""
        SELECT
            mo.name,
            mo.order_date,
            mo.status,
            mo.payment_status,
            mo.total_amount,
            mo.net_amount,
            mo.delivery_city,
            (SELECT COUNT(*) FROM `tabOrder Item` oi WHERE oi.parent = mo.name) as item_count
        FROM
            `tabMarketplace Order` mo
        WHERE
            mo.customer = %s AND mo.docstatus < 2
        ORDER BY
            mo.creation DESC
        LIMIT %s OFFSET %s
    """, (customer, page_size, offset), as_dict=True)
    
    return {"orders": orders, "total": total, "page": page, "page_size": page_size}


# ==================== QUOTE/ENQUIRY APIS ====================

@frappe.whitelist(allow_guest=True)
def create_quote_request(customer_name, email, phone, material=None, quantity=None, description=None, delivery_address=None):
    """Create a customer enquiry / quote request from the website"""
    if not customer_name or not email:
        frappe.throw(_("Name and email are required"))
    
    # Find or create customer
    customer = frappe.db.get_value("Marketplace Customer", {"email": email}, "name")
    if not customer:
        customer_doc = frappe.get_doc({
            "doctype": "Marketplace Customer",
            "customer_name": customer_name,
            "email": email,
            "phone": phone or "",
            "customer_type": "Individual"
        })
        customer_doc.insert(ignore_permissions=True)
        customer = customer_doc.name
    
    # Create enquiry
    enquiry = frappe.get_doc({
        "doctype": "Customer Enquiry",
        "customer": customer,
        "contact_number": phone or "",
        "email": email,
        "enquiry_date": nowdate(),
        "status": "Open",
        "material": material or "",
        "quantity": flt(quantity) if quantity else 0,
        "delivery_address": delivery_address or "",
        "description": description or "Quote request from website"
    })
    enquiry.insert(ignore_permissions=True)
    
    return {
        "success": True,
        "enquiry_id": enquiry.name,
        "message": _("Your quote request has been submitted successfully. We will contact you shortly.")
    }


# ==================== CART APIS ====================

@frappe.whitelist()
def get_cart():
    """Get the current user's cart items (stored as a simple json in session)"""
    cart = frappe.cache().hget(f"cart_{frappe.session.user}", "items")
    if not cart:
        return {"items": [], "total": 0}
    
    cart_items = frappe.parse_json(cart) if isinstance(cart, str) else cart
    total = sum(flt(item.get('amount', 0)) for item in cart_items)
    
    return {"items": cart_items, "total": total}


@frappe.whitelist()
def add_to_cart(material_id, price_id, quantity=1):
    """Add an item to the cart"""
    if frappe.session.user == "Guest":
        frappe.throw(_("Please login to add items to cart"), frappe.PermissionError)
    
    material = frappe.get_doc("Construction Material", material_id)
    price = frappe.get_doc("Material Price", price_id)
    
    cart = frappe.cache().hget(f"cart_{frappe.session.user}", "items")
    cart_items = frappe.parse_json(cart) if cart and isinstance(cart, str) else (cart or [])
    if not isinstance(cart_items, list):
        cart_items = []
    
    # Check if item already in cart
    existing = False
    for item in cart_items:
        if item.get('material_id') == material_id and item.get('price_id') == price_id:
            item['quantity'] = flt(item.get('quantity', 0)) + flt(quantity)
            item['amount'] = flt(item['quantity']) * flt(item.get('rate', 0))
            existing = True
            break
    
    if not existing:
        cart_items.append({
            "material_id": material.name,
            "material_name": material.material_name,
            "price_id": price.name,
            "supplier": price.supplier_name,
            "supplier_id": price.supplier,
            "rate": price.price_per_unit,
            "uom": price.unit_of_measure,
            "quantity": flt(quantity),
            "amount": flt(quantity) * price.price_per_unit,
            "min_qty": price.minimum_order_qty or 1
        })
    
    frappe.cache().hset(f"cart_{frappe.session.user}", "items", json.dumps(cart_items))
    
    total = sum(flt(item.get('amount', 0)) for item in cart_items)
    
    return {
        "success": True,
        "items": cart_items,
        "total": total,
        "item_count": len(cart_items),
        "message": _("{0} added to cart").format(material.material_name)
    }


@frappe.whitelist()
def remove_from_cart(material_id, price_id):
    """Remove an item from the cart"""
    cart = frappe.cache().hget(f"cart_{frappe.session.user}", "items")
    cart_items = frappe.parse_json(cart) if cart and isinstance(cart, str) else (cart or [])
    if not isinstance(cart_items, list):
        cart_items = []
    
    cart_items = [item for item in cart_items if not (item.get('material_id') == material_id and item.get('price_id') == price_id)]
    
    frappe.cache().hset(f"cart_{frappe.session.user}", "items", json.dumps(cart_items))
    
    total = sum(flt(item.get('amount', 0)) for item in cart_items)
    
    return {
        "success": True,
        "items": cart_items,
        "total": total,
        "item_count": len(cart_items)
    }


@frappe.whitelist()
def update_cart_qty(material_id, price_id, quantity):
    """Update quantity of a cart item"""
    quantity = flt(quantity)
    if quantity <= 0:
        return remove_from_cart(material_id, price_id)
    
    cart = frappe.cache().hget(f"cart_{frappe.session.user}", "items")
    cart_items = frappe.parse_json(cart) if cart and isinstance(cart, str) else (cart or [])
    if not isinstance(cart_items, list):
        cart_items = []
    
    for item in cart_items:
        if item.get('material_id') == material_id and item.get('price_id') == price_id:
            item['quantity'] = quantity
            item['amount'] = quantity * flt(item.get('rate', 0))
            break
    
    frappe.cache().hset(f"cart_{frappe.session.user}", "items", json.dumps(cart_items))
    
    total = sum(flt(item.get('amount', 0)) for item in cart_items)
    
    return {
        "success": True,
        "items": cart_items,
        "total": total,
        "item_count": len(cart_items)
    }


# ==================== ORDER APIS ====================

@frappe.whitelist()
def place_order(delivery_address=None, delivery_city=None, delivery_contact=None, delivery_phone=None, notes=None):
    """Place an order from cart items"""
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Please login to place an order"), frappe.PermissionError)
    
    # Get customer
    customer = frappe.db.get_value("Marketplace Customer", {"email": user}, "name")
    if not customer:
        frappe.throw(_("Customer profile not found. Please create a profile first."))
    
    # Get cart
    cart = frappe.cache().hget(f"cart_{frappe.session.user}", "items")
    cart_items = frappe.parse_json(cart) if cart and isinstance(cart, str) else (cart or [])
    
    if not cart_items or len(cart_items) == 0:
        frappe.throw(_("Cart is empty"))
    
    # Create order
    order = frappe.get_doc({
        "doctype": "Marketplace Order",
        "naming_series": "MORD-.YYYY.-",
        "customer": customer,
        "order_date": nowdate(),
        "status": "Draft",
        "delivery_address": delivery_address or "",
        "delivery_city": delivery_city or "",
        "delivery_contact": delivery_contact or "",
        "delivery_phone": delivery_phone or "",
        "notes": notes or ""
    })
    
    for item in cart_items:
        order.append("items", {
            "item_code": item.get("material_id"),
            "quantity": flt(item.get("quantity", 1)),
            "rate": flt(item.get("rate", 0))
        })
    
    order.insert(ignore_permissions=True)
    
    # Clear cart
    frappe.cache().hdel(f"cart_{frappe.session.user}", "items")
    
    return {
        "success": True,
        "order_id": order.name,
        "message": _("Order {0} has been placed successfully!").format(order.name)
    }


# ==================== PROJECT APIS ====================

@frappe.whitelist(allow_guest=True)
def get_projects(page=1, page_size=12):
    """Get marketplace orders as sample projects for showcase"""
    page = int(page)
    page_size = int(page_size)
    offset = (page - 1) * page_size
    
    conditions = ["mo.docstatus < 2"]
    
    total = frappe.db.sql(f"""
        SELECT COUNT(*) as total
        FROM `tabMarketplace Order` mo
        WHERE {' AND '.join(conditions)}
    """, as_dict=True)[0].total
    
    projects = frappe.db.sql(f"""
        SELECT
            mo.name as project_id,
            mo.customer_name,
            mo.order_date,
            mo.delivery_date,
            mo.delivery_city,
            mo.total_amount,
            mo.status,
            (SELECT COUNT(*) FROM `tabOrder Item` oi WHERE oi.parent = mo.name) as item_count
        FROM
            `tabMarketplace Order` mo
        WHERE {' AND '.join(conditions)}
        ORDER BY mo.creation DESC
        LIMIT {page_size} OFFSET {offset}
    """, as_dict=True)
    
    return {
        "projects": projects,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, -(-total // page_size))
    }


# ==================== DASHBOARD STATS ====================

@frappe.whitelist()
def get_dashboard_stats():
    """Get stats for the customer dashboard"""
    user = frappe.session.user
    if user == "Guest":
        return {}
    
    customer = frappe.db.get_value("Marketplace Customer", {"email": user}, "name")
    if not customer:
        return {}
    
    orders_count = frappe.db.count("Marketplace Order", {"customer": customer})
    enquiries_count = frappe.db.count("Customer Enquiry", {"customer": customer})
    
    return {
        "orders_count": orders_count,
        "enquiries_count": enquiries_count,
        "customer_name": frappe.db.get_value("Marketplace Customer", customer, "customer_name")
    }


@frappe.whitelist()
def get_supplier_dashboard_stats():
    """Get stats for the supplier dashboard"""
    user = frappe.session.user
    if user == "Guest":
        return {}
    
    supplier = frappe.db.get_value("Supplier", {"email": user}, "name")
    if not supplier:
        return {}
    
    products_count = frappe.db.count("Material Price", {"supplier": supplier})
    
    return {
        "products_count": products_count,
        "supplier_name": frappe.db.get_value("Supplier", supplier, "supplier_name"),
        "rating": frappe.db.get_value("Supplier", supplier, "rating")
    }


# ==================== WEBSITE UTILITY APIS ====================

@frappe.whitelist(allow_guest=True)
def get_featured_materials(limit=8):
    """Get featured/random materials for homepage"""
    materials = frappe.db.sql("""
        SELECT
            cm.name as material_id,
            cm.material_name,
            cm.brand,
            cm.unit_of_measure,
            cm.image,
            cm.description,
            mc.title as category,
            (SELECT MIN(mp.price_per_unit) FROM `tabMaterial Price` mp 
             WHERE mp.material = cm.name AND mp.is_active = 1 AND mp.docstatus < 2) as min_price
        FROM
            `tabConstruction Material` cm
        LEFT JOIN
            `tabMaterial Category` mc ON cm.material_category = mc.name
        WHERE
            cm.is_active = 1 AND cm.docstatus < 2
        ORDER BY
            RAND()
        LIMIT %s
    """, int(limit), as_dict=True)
    
    return materials


@frappe.whitelist(allow_guest=True)
def get_top_suppliers(limit=6):
    """Get top-rated suppliers for homepage"""
    suppliers = frappe.db.sql("""
        SELECT
            s.name as supplier_id,
            s.supplier_name,
            s.company_name,
            s.rating,
            s.city,
            s.email,
            s.phone,
            (SELECT COUNT(*) FROM `tabMaterial Price` mp 
             WHERE mp.supplier = s.name AND mp.is_active = 1 AND mp.docstatus < 2) as product_count
        FROM
            `tabSupplier` s
        WHERE
            s.is_approved = 1 AND s.docstatus < 2 AND s.rating IS NOT NULL
        ORDER BY
            s.rating DESC
        LIMIT %s
    """, int(limit), as_dict=True)
    
    return suppliers


@frappe.whitelist(allow_guest=True)
def get_testimonials(limit=4):
    """Get sample testimonials"""
    testimonials = [
        {
            "name": "Rajesh Kumar",
            "role": "Builder, Pune",
            "content": "Excellent platform for sourcing construction materials. The pricing is competitive and delivery is always on time.",
            "rating": 5
        },
        {
            "name": "Priya Sharma",
            "role": "Contractor, Bangalore",
            "content": "I found the best suppliers for my project through this marketplace. Highly recommended for all construction needs.",
            "rating": 5
        },
        {
            "name": "Arun Nair",
            "role": "Architect, Mumbai",
            "content": "The material catalog is comprehensive and easy to navigate. Saves a lot of time in procurement.",
            "rating": 4
        },
        {
            "name": "Vikram Singh",
            "role": "Interior Designer, Delhi",
            "content": "Great variety of materials and finishes. The quality check process gives me confidence in every order.",
            "rating": 5
        }
    ]
    
    return testimonials[:int(limit)]
