# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import random

import frappe
from frappe import _
from frappe.utils import nowdate, add_days, flt, getdate


def create_demo_data():
    """
    Create comprehensive demo data for the Construction Marketplace application.
    Run via: bench --site your-site execute construction_marketplace.demo.create_demo_data

    This function creates:
    - 17 Construction Materials (8 from install.py + 9 additional)
    - 8 Suppliers
    - 8 Marketplace Customers
    - 25 Material Prices
    - 15 Marketplace Orders with items
    - 12 Customer Enquiries
    - 10 Purchase Orders with items
    - 10 Material Requests with items
    - 10 Delivery Schedules with items
    - 10 Quality Checks with parameters
    - Marketplace Settings (Single)
    """
    print("=" * 60)
    print("  CONSTRUCTION MARKETPLACE - DEMO DATA CREATION")
    print("=" * 60)

    # Step 0: Fix child table modules so Frappe can find controllers
    _ensure_base_setup()

    # Step 1: Create/ensure Materials (12 total)
    materials = _create_materials()

    # Step 2: Create Suppliers (8)
    suppliers = _create_suppliers()

    # Step 3: Create Marketplace Customers (8)
    customers = _create_customers()

    # Step 4: Create Material Prices (25)
    prices = _create_prices(materials, suppliers)
    del prices  # Not directly used further

    # Step 5: Generate routes for all materials
    _generate_routes()

    # Step 6: Create Marketplace Orders (15)
    orders = _create_orders(customers, materials)

    # Step 7: Create Customer Enquiries (12)
    enquiries = _create_enquiries(customers, materials)
    del enquiries  # Not directly used further

    # Step 8: Create Purchase Orders (10)
    purchase_orders = _create_purchase_orders(suppliers, materials, orders)

    # Step 9: Create Material Requests (10)
    material_requests = _create_material_requests(materials)
    del material_requests  # Not directly used further

    # Step 10: Create Delivery Schedules (10)
    delivery_schedules = _create_delivery_schedules(orders, materials)
    del delivery_schedules  # Not directly used further

    # Step 11: Create Quality Checks (10)
    quality_checks = _create_quality_checks(materials, suppliers, orders)
    del quality_checks  # Not directly used further

    # Step 12: Setup Marketplace Settings
    _setup_marketplace_settings()

    # Link some purchase orders to marketplace orders and material requests
    _link_related_docs(purchase_orders, orders)

    frappe.db.commit()

    print("=" * 60)
    print("  ✅  DEMO DATA CREATION COMPLETE")
    print("=" * 60)
    print(f"   Materials:         17")
    print(f"   Suppliers:          8")
    print(f"   Customers:          8")
    print(f"   Prices:            25")
    print(f"   Orders:            15")
    print(f"   Enquiries:         12")
    print(f"   Purchase Orders:   10")
    print(f"   Material Requests: 10")
    print(f"   Deliveries:        10")
    print(f"   Quality Checks:    10")
    print("=" * 60)


def _ensure_base_setup():
    """Run base setup functions from install.py to ensure base data exists."""
    from construction_marketplace.install import (
        create_default_roles,
        create_default_categories,
        create_default_grades,
        create_demo_materials,
        _fix_child_table_modules,
    )

    _fix_child_table_modules()
    print("\n📋 Ensuring base data exists...")
    create_default_roles()
    create_default_categories()
    create_default_grades()
    create_demo_materials()
    print("✅ Base setup complete\n")


# ---------------------------------------------------------------------------
# Step 1 — Materials (12 total: 8 from install.py + 4 new)
# ---------------------------------------------------------------------------

def _create_materials():
    """Ensure all 12 materials exist and return mapped dict."""
    materials = {}

    # These 8 are already created by create_demo_materials() in install.py
    base_materials = [
        ("Ultratech PPC Cement - PPC Grade", "PPC Grade", "Cement"),
        ("ACC OPC 53 Grade Cement - OPC 53 Grade", "OPC 53 Grade", "Cement"),
        ("JSW Fe 500D TMT Steel - Fe 500D", "Fe 500D", "TMT Steel"),
        ("Tata Tiscon Fe 500 TMT Steel - Fe 500", "Fe 500", "TMT Steel"),
        ("M Sand for Plastering - Plastering M Sand", "Plastering M Sand", "M Sand"),
        ("M Sand for Concrete - Concrete M Sand", "Concrete M Sand", "M Sand"),
        ("Wirecut Red Bricks - Wirecut Bricks", "Wirecut Bricks", "Bricks"),
        ("AAC Lightweight Blocks - AAC Lightweight", "AAC Lightweight", "Blocks"),
    ]

    for title, _, _ in base_materials:
        name = frappe.db.get_value("Construction Material", {"title": title}, "name")
        if name:
            materials[title] = name

    # Add 4 additional materials
    additional = [
        {
            "material_name": "Birla Gold OPC 43 Grade Cement",
            "category": "Cement",
            "grade": "OPC 43 Grade",
            "brand": "Birla Gold",
            "uom": "Bag",
            "reorder_level": 50,
            "current_stock": 200,
            "description": "<p>Birla Gold OPC 43 Grade Cement, suitable for general construction purposes including plastering, flooring, and masonry.</p>",
        },
        {
            "material_name": "JSW Fe 550 TMT Steel",
            "category": "TMT Steel",
            "grade": "Fe 550",
            "brand": "JSW",
            "uom": "Ton",
            "reorder_level": 5,
            "current_stock": 25,
            "description": "<p>JSW Fe 550 Grade TMT steel bars with superior strength for high-rise construction and heavy structures.</p>",
        },
        {
            "material_name": "Table Mould Red Bricks",
            "category": "Bricks",
            "grade": "Table Mould",
            "brand": "Standard",
            "uom": "Pieces",
            "reorder_level": 2000,
            "current_stock": 10000,
            "description": "<p>Table mould red bricks, machine-pressed for uniform size and shape. Ideal for walls and partitions.</p>",
        },
        {
            "material_name": "Solid Concrete Blocks",
            "category": "Blocks",
            "grade": "Solid Concrete Blocks",
            "brand": "Buildmate",
            "uom": "Pieces",
            "reorder_level": 500,
            "current_stock": 2500,
            "description": "<p>Solid concrete blocks 4-inch size for load-bearing walls and structural applications.</p>",
        },
        {
            "material_name": "Ambuja PSC Grade Cement",
            "category": "Cement",
            "grade": "PSC Grade",
            "brand": "Ambuja",
            "uom": "Bag",
            "reorder_level": 50,
            "current_stock": 300,
            "description": "<p>Ambuja PSC (Portland Slag Cement) Grade Cement, ideal for marine structures, mass concreting, and hydraulic structures due to its superior durability and low heat of hydration.</p>",
        },
        {
            "material_name": "SAIL Fe 550D TMT Steel",
            "category": "TMT Steel",
            "grade": "Fe 550D",
            "brand": "SAIL",
            "uom": "Ton",
            "reorder_level": 5,
            "current_stock": 30,
            "description": "<p>SAIL Fe 550D Grade TMT steel with high ductility for earthquake-resistant structures. Excellent weldability and bendability.</p>",
        },
        {
            "material_name": "Traditional Red Bricks",
            "category": "Bricks",
            "grade": "Red Bricks",
            "brand": "Standard",
            "uom": "Pieces",
            "reorder_level": 2000,
            "current_stock": 15000,
            "description": "<p>Traditional chamber red bricks, kiln-fired for strength and durability. Standard size 9x4x3 inches, suitable for load-bearing walls.</p>",
        },
        {
            "material_name": "20mm Crushed Jelly Stones",
            "category": "Jelly Stones",
            "grade": "",
            "brand": "Premium",
            "uom": "Ton",
            "reorder_level": 10,
            "current_stock": 50,
            "description": "<p>20mm crushed stone aggregates (jelly stones) for concrete mixing. Sourced from granite quarries, washed and graded for quality.</p>",
        },
        {
            "material_name": "Galvanized Binding Wire",
            "category": "Other Materials",
            "grade": "",
            "brand": "Standard",
            "uom": "Kg",
            "reorder_level": 100,
            "current_stock": 500,
            "description": "<p>Galvanized iron binding wire for TMT steel tying and reinforcement works. 16 gauge, rust-resistant coating.</p>",
        },
    ]

    for mat in additional:
        cat = frappe.db.get_value("Material Category", {"title": mat["category"]}, "name")
        if not cat:
            print(f"⚠️  Skipping {mat['material_name']}: category '{mat['category']}' not found")
            continue

        # Grade is optional (material_grade field is not reqd in the doctype)
        grade = None
        if mat["grade"]:
            grade = frappe.db.get_value("Material Grade", {"grade_name": mat["grade"]}, "name")
            if not grade:
                print(f"  ⚠️  Grade '{mat['grade']}' not found for {mat['material_name']}, creating without grade")

        # Build title with grade suffix only when a grade exists
        title = mat["material_name"] if not mat["grade"] else f"{mat['material_name']} - {mat['grade']}"

        existing = frappe.db.get_value("Construction Material", {"title": title}, "name")
        if existing:
            materials[title] = existing
            continue

        doc_dict = {
            "doctype": "Construction Material",
            "material_name": mat["material_name"],
            "title": title,
            "material_category": cat,
            "brand": mat["brand"],
            "unit_of_measure": mat["uom"],
            "reorder_level": mat["reorder_level"],
            "current_stock": mat["current_stock"],
            "last_restock_date": add_days(nowdate(), -random.randint(1, 30)),
            "is_active": 1,
            "description": mat.get("description", ""),
            "specifications": [],
        }
        # Only set material_grade if one was found
        if grade:
            doc_dict["material_grade"] = grade

        doc = frappe.get_doc(doc_dict)
        frappe.flags.in_import = True
        doc.insert(ignore_permissions=True)
        frappe.flags.in_import = False
        materials[title] = doc.name
        print(f"  ✅ Created material: {mat['material_name']}")

    print(f"✅ Materials: {len(materials)} total\n")
    return materials


# ---------------------------------------------------------------------------
# Step 2 — Suppliers (8)
# ---------------------------------------------------------------------------

def _create_suppliers():
    """Create 8 suppliers, return dict mapping name → docname."""
    supplier_data = [
        {
            "supplier_name": "BuildMart Supplies",
            "company_name": "BuildMart Pvt Ltd",
            "contact_person": "Ramesh Kumar",
            "email": "ramesh@buildmart.com",
            "phone": "9876543210",
            "mobile": "9876543210",
            "address": "42, Industrial Area, Andheri East",
            "city": "Mumbai",
            "state": "Maharashtra",
            "pincode": "400093",
            "country": "India",
            "gst_number": "27AABCU1234D1Z5",
            "website": "https://buildmart.com",
            "rating": 4.5,
            "is_approved": 1,
            "bank_details": "<p>Bank: HDFC Bank<br>Branch: Andheri East<br>Account: 50100123456789<br>IFSC: HDFC0001234</p>",
        },
        {
            "supplier_name": "SteelKing Distributors",
            "company_name": "SteelKing Ltd",
            "contact_person": "Amit Singh",
            "email": "amit@steelking.com",
            "phone": "9876543211",
            "mobile": "9876543211",
            "address": "Plot 15, Okhla Industrial Estate, Phase II",
            "city": "Delhi",
            "state": "Delhi",
            "pincode": "110020",
            "country": "India",
            "gst_number": "07AABCU5678E1Z5",
            "website": "https://steelking.com",
            "rating": 4.2,
            "is_approved": 1,
            "bank_details": "<p>Bank: ICICI Bank<br>Branch: Okhla<br>Account: 60100234567890<br>IFSC: ICIC0002345</p>",
        },
        {
            "supplier_name": "Prime Cement Traders",
            "company_name": "Prime Cement Traders",
            "contact_person": "Suresh Patel",
            "email": "suresh@primecement.com",
            "phone": "9876543212",
            "mobile": "9876543212",
            "address": "55, SG Highway, Bodakdev",
            "city": "Ahmedabad",
            "state": "Gujarat",
            "pincode": "380054",
            "country": "India",
            "gst_number": "24AABCU9012K1Z5",
            "website": "https://primecement.com",
            "rating": 4.8,
            "is_approved": 1,
            "bank_details": "<p>Bank: Axis Bank<br>Branch: Bodakdev<br>Account: 70100345678901<br>IFSC: AXIS0003456</p>",
        },
        {
            "supplier_name": "Sand Depot",
            "company_name": "Sand Depot Pvt Ltd",
            "contact_person": "Vikram Reddy",
            "email": "vikram@sanddepot.com",
            "phone": "9876543213",
            "mobile": "9876543213",
            "address": "88, Nacharam Industrial Area",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500076",
            "country": "India",
            "gst_number": "36AABCS1234H1Z5",
            "website": "https://sanddepot.com",
            "rating": 4.0,
            "is_approved": 1,
            "bank_details": "<p>Bank: SBI<br>Branch: Nacharam<br>Account: 40100567890123<br>IFSC: SBIN0004567</p>",
        },
        {
            "supplier_name": "BrickHouse Bricks",
            "company_name": "BrickHouse Bricks Ltd",
            "contact_person": "Mohan Das",
            "email": "mohan@brickhouse.com",
            "phone": "9876543214",
            "mobile": "9876543214",
            "address": "12, Ambattur Industrial Estate",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "pincode": "600058",
            "country": "India",
            "gst_number": "33AABCU3456F1Z5",
            "website": "https://brickhouse.com",
            "rating": 4.3,
            "is_approved": 1,
            "bank_details": "<p>Bank: Canara Bank<br>Branch: Ambattur<br>Account: 30100789012345<br>IFSC: CNRB0005678</p>",
        },
        {
            "supplier_name": "TransCon Logistics & Supply",
            "company_name": "TransCon Logistics Pvt Ltd",
            "contact_person": "Arun Mehta",
            "email": "arun@transcon.com",
            "phone": "9876543215",
            "mobile": "9876543215",
            "address": "Plot 7, Sector 12, Nerul",
            "city": "Navi Mumbai",
            "state": "Maharashtra",
            "pincode": "400706",
            "country": "India",
            "gst_number": "27AABCT7890M1Z5",
            "rating": 3.8,
            "is_approved": 1,
            "bank_details": "<p>Bank: Kotak Mahindra<br>Branch: Nerul<br>Account: 80100901234567<br>IFSC: KKBK0006789</p>",
        },
        {
            "supplier_name": "Apex Building Materials",
            "company_name": "Apex Building Materials",
            "contact_person": "Kavita Joshi",
            "email": "kavita@apexbuild.com",
            "phone": "9876543216",
            "mobile": "9876543216",
            "address": "25, Baner Road",
            "city": "Pune",
            "state": "Maharashtra",
            "pincode": "411045",
            "country": "India",
            "gst_number": "27AABCA1234P1Z5",
            "rating": 4.6,
            "is_approved": 0,
            "bank_details": "<p>Bank: HDFC Bank<br>Branch: Baner<br>Account: 50100789012345<br>IFSC: HDFC0007890</p>",
        },
        {
            "supplier_name": "Metro Constructions Supply",
            "company_name": "Metro Constructions Supply Co",
            "contact_person": "Dinesh Yadav",
            "email": "dinesh@metroconstructions.com",
            "phone": "9876543217",
            "address": "56, BTM Layout, Stage 2",
            "city": "Bangalore",
            "state": "Karnataka",
            "pincode": "560076",
            "country": "India",
            "gst_number": "29AABCM5678K1Z5",
            "rating": 4.1,
            "is_approved": 1,
            "bank_details": "<p>Bank: Yes Bank<br>Branch: BTM Layout<br>Account: 90100456789012<br>IFSC: YESB0008901</p>",
        },
    ]

    suppliers = {}
    for s in supplier_data:
        existing = frappe.db.get_value("Supplier", {"supplier_name": s["supplier_name"]}, "name")
        if existing:
            suppliers[s["supplier_name"]] = existing
            continue

        doc = frappe.get_doc({
            "doctype": "Supplier",
            "supplier_name": s["supplier_name"],
            "company_name": s.get("company_name"),
            "contact_person": s.get("contact_person"),
            "email": s.get("email"),
            "phone": s.get("phone"),
            "mobile": s.get("mobile"),
            "address": s.get("address"),
            "city": s.get("city"),
            "state": s.get("state"),
            "pincode": s.get("pincode"),
            "country": s.get("country", "India"),
            "gst_number": s.get("gst_number"),
            "website": s.get("website"),
            "rating": s.get("rating"),
            "is_approved": s.get("is_approved", 0),
            "bank_details": s.get("bank_details", ""),
        })
        doc.insert(ignore_permissions=True)
        suppliers[s["supplier_name"]] = doc.name
        print(f"  ✅ Created supplier: {s['supplier_name']}")

    print(f"✅ Suppliers: {len(suppliers)}\n")
    return suppliers


# ---------------------------------------------------------------------------
# Step 3 — Marketplace Customers (8)
# ---------------------------------------------------------------------------

def _create_customers():
    """Create 8 marketplace customers, return dict mapping name → docname."""
    customer_data = [
        {
            "customer_name": "Raj Constructions",
            "company_name": "Raj Constructions Pvt Ltd",
            "customer_type": "Builder",
            "contact_person": "Rajesh Verma",
            "email": "rajesh@rajconstructions.com",
            "phone": "9988776655",
            "mobile": "9988776655",
            "address": "25, MG Road, Camp",
            "city": "Pune",
            "state": "Maharashtra",
            "pincode": "411001",
            "gst_number": "27AABCR1234D1Z5",
            "is_verified": 1,
            "notes": "<p>Premium builder with multiple ongoing projects in Pune region.</p>",
        },
        {
            "customer_name": "Greenfield Developers",
            "company_name": "Greenfield Developers",
            "customer_type": "Contractor",
            "contact_person": "Priya Sharma",
            "email": "priya@greenfield.com",
            "phone": "9988776666",
            "mobile": "9988776666",
            "address": "88, Koramangala Industrial Layout",
            "city": "Bangalore",
            "state": "Karnataka",
            "pincode": "560034",
            "gst_number": "29AABCG5678H1Z5",
            "is_verified": 1,
            "notes": "<p>Specializes in green building and sustainable construction projects.</p>",
        },
        {
            "customer_name": "Urban Infrastructure",
            "company_name": "Urban Infrastructure Ltd",
            "customer_type": "Builder",
            "contact_person": "Arun Nair",
            "email": "arun@urbaninfra.com",
            "phone": "9988776677",
            "mobile": "9988776677",
            "address": "Plot 15, Bandra Kurla Complex",
            "city": "Mumbai",
            "state": "Maharashtra",
            "pincode": "400051",
            "gst_number": "27AABCU9012K1Z5",
            "is_verified": 1,
            "notes": "<p>Large infrastructure developer working on commercial and residential towers.</p>",
        },
        {
            "customer_name": "Skyline Builders",
            "company_name": "Skyline Builders & Developers",
            "customer_type": "Builder",
            "contact_person": "Sandeep Reddy",
            "email": "sandeep@skylinebuilders.com",
            "phone": "9988776688",
            "address": "12, Jubilee Hills Road 36",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500033",
            "gst_number": "36AABCS1234K1Z5",
            "is_verified": 1,
            "notes": "<p>Leading residential builder in Hyderabad with 5+ ongoing projects.</p>",
        },
        {
            "customer_name": "Blueprint Architects",
            "company_name": "Blueprint Architects & Planners",
            "customer_type": "Architect",
            "contact_person": "Ananya Krishnan",
            "email": "ananya@blueprintarch.com",
            "phone": "9988776699",
            "address": "45, Cathedral Road, Gopalapuram",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "pincode": "600086",
            "gst_number": "33AABCB3456F1Z5",
            "is_verified": 0,
        },
        {
            "customer_name": "Apex Constructions",
            "company_name": "Apex Constructions Co",
            "customer_type": "Contractor",
            "contact_person": "Vijay Singh",
            "email": "vijay@apexconstructions.com",
            "phone": "9988776600",
            "address": "78, Lajpat Nagar, Part 2",
            "city": "Delhi",
            "state": "Delhi",
            "pincode": "110024",
            "gst_number": "07AABCA5678D1Z5",
            "is_verified": 1,
        },
        {
            "customer_name": "Nova Interiors",
            "company_name": "Nova Interiors & Designs",
            "customer_type": "Business",
            "contact_person": "Meera Patel",
            "email": "meera@novainteriors.com",
            "phone": "9988776611",
            "address": "33, CG Road, Navrangpura",
            "city": "Ahmedabad",
            "state": "Gujarat",
            "pincode": "380009",
            "gst_number": "24AABCN7890K1Z5",
            "is_verified": 0,
        },
        {
            "customer_name": "Patel & Sons Construction",
            "company_name": "Patel & Sons Construction",
            "customer_type": "Builder",
            "contact_person": "Hitesh Patel",
            "email": "hitesh@patelandsons.com",
            "phone": "9988776622",
            "address": "1, Adajan Patia",
            "city": "Surat",
            "state": "Gujarat",
            "pincode": "395009",
            "gst_number": "24AABCP9012L1Z5",
            "is_verified": 1,
        },
    ]

    customers = {}
    for c in customer_data:
        existing = frappe.db.get_value("Marketplace Customer", {"customer_name": c["customer_name"]}, "name")
        if existing:
            customers[c["customer_name"]] = existing
            continue

        doc = frappe.get_doc({
            "doctype": "Marketplace Customer",
            "customer_name": c["customer_name"],
            "company_name": c.get("company_name"),
            "customer_type": c.get("customer_type"),
            "contact_person": c.get("contact_person"),
            "email": c.get("email"),
            "phone": c.get("phone"),
            "mobile": c.get("mobile"),
            "address": c.get("address"),
            "city": c.get("city"),
            "state": c.get("state"),
            "pincode": c.get("pincode"),
            "country": c.get("country", "India"),
            "gst_number": c.get("gst_number"),
            "is_verified": c.get("is_verified", 0),
            "verification_date": nowdate() if c.get("is_verified") else None,
            "notes": c.get("notes", ""),
        })
        doc.insert(ignore_permissions=True)
        customers[c["customer_name"]] = doc.name
        print(f"  ✅ Created customer: {c['customer_name']}")

    print(f"✅ Customers: {len(customers)}\n")
    return customers


# ---------------------------------------------------------------------------
# Step 4 — Material Prices (25)
# ---------------------------------------------------------------------------

def _create_prices(materials, suppliers):
    """Create 25 material price records across all materials and suppliers."""
    price_defs = [
        # Cement prices
        ("Ultratech PPC Cement - PPC Grade", "BuildMart Supplies", 350, 10),
        ("Ultratech PPC Cement - PPC Grade", "Prime Cement Traders", 340, 20),
        ("Ultratech PPC Cement - PPC Grade", "Apex Building Materials", 345, 15),
        ("ACC OPC 53 Grade Cement - OPC 53 Grade", "BuildMart Supplies", 380, 10),
        ("ACC OPC 53 Grade Cement - OPC 53 Grade", "Prime Cement Traders", 370, 20),
        ("ACC OPC 53 Grade Cement - OPC 53 Grade", "TransCon Logistics & Supply", 375, 15),
        ("Birla Gold OPC 43 Grade Cement - OPC 43 Grade", "Prime Cement Traders", 330, 20),
        ("Birla Gold OPC 43 Grade Cement - OPC 43 Grade", "BuildMart Supplies", 340, 10),
        # TMT Steel prices
        ("JSW Fe 500D TMT Steel - Fe 500D", "SteelKing Distributors", 68000, 1),
        ("JSW Fe 500D TMT Steel - Fe 500D", "Metro Constructions Supply", 67500, 2),
        ("Tata Tiscon Fe 500 TMT Steel - Fe 500", "SteelKing Distributors", 65000, 1),
        ("Tata Tiscon Fe 500 TMT Steel - Fe 500", "BuildMart Supplies", 65500, 1),
        ("JSW Fe 550 TMT Steel - Fe 550", "SteelKing Distributors", 72000, 1),
        ("JSW Fe 550 TMT Steel - Fe 550", "Metro Constructions Supply", 71500, 2),
        # M Sand prices
        ("M Sand for Plastering - Plastering M Sand", "Sand Depot", 45, 50),
        ("M Sand for Plastering - Plastering M Sand", "BuildMart Supplies", 48, 50),
        ("M Sand for Concrete - Concrete M Sand", "Sand Depot", 52, 50),
        ("M Sand for Concrete - Concrete M Sand", "TransCon Logistics & Supply", 50, 50),
        # Bricks & Blocks prices
        ("Wirecut Red Bricks - Wirecut Bricks", "BrickHouse Bricks", 8, 500),
        ("Wirecut Red Bricks - Wirecut Bricks", "BuildMart Supplies", 8.5, 500),
        ("Table Mould Red Bricks - Table Mould", "BrickHouse Bricks", 7, 500),
        ("Table Mould Red Bricks - Table Mould", "Apex Building Materials", 7.2, 500),
        ("AAC Lightweight Blocks - AAC Lightweight", "BuildMart Supplies", 55, 100),
        ("AAC Lightweight Blocks - AAC Lightweight", "Apex Building Materials", 53, 100),
        ("Solid Concrete Blocks - Solid Concrete Blocks", "BrickHouse Bricks", 35, 100),
    ]

    created = 0
    existing = 0
    for mat_title, supp_name, price, min_qty in price_defs:
        material = materials.get(mat_title)
        supplier = suppliers.get(supp_name)
        if not material or not supplier:
            print(f"  ⚠️  Skipping price: {mat_title} @ {supp_name} (missing reference)")
            continue

        # Check if this price record already exists
        existing_price = frappe.db.get_value(
            "Material Price",
            {"material": material, "supplier": supplier},
            "name",
        )
        if existing_price:
            existing += 1
            continue

        # Get unit_of_measure from material
        uom = frappe.db.get_value("Construction Material", material, "unit_of_measure")

        doc = frappe.get_doc({
            "doctype": "Material Price",
            "material": material,
            "supplier": supplier,
            "price_per_unit": price,
            "unit_of_measure": uom,
            "minimum_order_qty": min_qty,
            "currency": "INR",
            "effective_from": add_days(nowdate(), -90),
            "effective_to": add_days(nowdate(), 275),
            "is_active": 1,
        })
        try:
            doc.insert(ignore_permissions=True)
            created += 1
        except frappe.DuplicateEntryError:
            existing += 1

    print(f"✅ Prices: {created} created, {existing} existing\n")


# ---------------------------------------------------------------------------
# Step 5 — Generate routes
# ---------------------------------------------------------------------------

def _generate_routes():
    """Generate URL routes for materials that don't have one."""
    from construction_marketplace.install import generate_material_routes
    generate_material_routes()


# ---------------------------------------------------------------------------
# Step 6 — Marketplace Orders (15)
# ---------------------------------------------------------------------------

def _create_orders(customers, materials):
    """Create 15 marketplace orders with items in various statuses."""
    now = nowdate()

    # Define order templates: (customer, days_ago, status, payment_status, payment_method,
    #                       delivery_city, items [(mat_title, qty, rate)])
    order_defs = [
        ("Raj Constructions", 45, "Delivered", "Completed", "UPI", "Pune", [
            ("Ultratech PPC Cement - PPC Grade", 50, 350),
            ("M Sand for Concrete - Concrete M Sand", 200, 52),
        ]),
        ("Raj Constructions", 30, "Delivered", "Completed", "Bank Transfer", "Pune", [
            ("JSW Fe 500D TMT Steel - Fe 500D", 3, 68000),
            ("Wirecut Red Bricks - Wirecut Bricks", 2000, 8),
        ]),
        ("Greenfield Developers", 20, "Shipped", "Partial", "UPI", "Bangalore", [
            ("ACC OPC 53 Grade Cement - OPC 53 Grade", 100, 380),
            ("M Sand for Plastering - Plastering M Sand", 300, 45),
            ("AAC Lightweight Blocks - AAC Lightweight", 500, 55),
        ]),
        ("Greenfield Developers", 15, "Processing", "Pending", "", "Bangalore", [
            ("JSW Fe 500D TMT Steel - Fe 500D", 5, 68000),
        ]),
        ("Urban Infrastructure", 10, "Confirmed", "Pending", "", "Mumbai", [
            ("ACC OPC 53 Grade Cement - OPC 53 Grade", 200, 380),
            ("Tata Tiscon Fe 500 TMT Steel - Fe 500", 8, 65000),
            ("M Sand for Concrete - Concrete M Sand", 400, 52),
        ]),
        ("Urban Infrastructure", 7, "Confirmed", "Pending", "", "Mumbai", [
            ("Ultratech PPC Cement - PPC Grade", 150, 350),
            ("Wirecut Red Bricks - Wirecut Bricks", 3000, 8),
        ]),
        ("Skyline Builders", 14, "Processing", "Partial", "Bank Transfer", "Hyderabad", [
            ("Table Mould Red Bricks - Table Mould", 5000, 7),
            ("M Sand for Plastering - Plastering M Sand", 500, 45),
        ]),
        ("Skyline Builders", 5, "Confirmed", "Pending", "", "Hyderabad", [
            ("JSW Fe 550 TMT Steel - Fe 550", 4, 72000),
        ]),
        ("Blueprint Architects", 12, "Shipped", "Completed", "Card", "Chennai", [
            ("Birla Gold OPC 43 Grade Cement - OPC 43 Grade", 80, 330),
            ("Solid Concrete Blocks - Solid Concrete Blocks", 800, 35),
        ]),
        ("Apex Constructions", 25, "Delivered", "Completed", "UPI", "Delhi", [
            ("Tata Tiscon Fe 500 TMT Steel - Fe 500", 6, 65000),
            ("Ultratech PPC Cement - PPC Grade", 100, 350),
        ]),
        ("Apex Constructions", 8, "Processing", "Pending", "", "Delhi", [
            ("ACC OPC 53 Grade Cement - OPC 53 Grade", 120, 380),
            ("M Sand for Concrete - Concrete M Sand", 250, 52),
            ("Wirecut Red Bricks - Wirecut Bricks", 1500, 8),
        ]),
        ("Nova Interiors", 6, "Confirmed", "Pending", "", "Ahmedabad", [
            ("Birla Gold OPC 43 Grade Cement - OPC 43 Grade", 40, 330),
            ("M Sand for Plastering - Plastering M Sand", 100, 45),
        ]),
        ("Patel & Sons Construction", 18, "Shipped", "Partial", "Bank Transfer", "Surat", [
            ("Ultratech PPC Cement - PPC Grade", 200, 350),
            ("JSW Fe 500D TMT Steel - Fe 500D", 4, 68000),
            ("M Sand for Concrete - Concrete M Sand", 300, 52),
        ]),
        ("Patel & Sons Construction", 3, "Draft", "Pending", "", "Surat", [
            ("Solid Concrete Blocks - Solid Concrete Blocks", 600, 35),
        ]),
        ("Raj Constructions", 2, "Draft", "Pending", "", "Pune", [
            ("AAC Lightweight Blocks - AAC Lightweight", 300, 55),
            ("Table Mould Red Bricks - Table Mould", 2000, 7),
        ]),
    ]

    orders = {}
    for cust_name, days_ago, status, pay_status, pay_method, del_city, items in order_defs:
        customer = customers.get(cust_name)
        if not customer:
            print(f"  ⚠️  Skipping order for {cust_name}: customer not found")
            continue

        order_date = add_days(now, -days_ago)
        delivery_date = add_days(order_date, random.randint(7, 30))

        # Calculate totals
        total_amount = 0
        order_items = []
        for mat_title, qty, rate in items:
            mat = materials.get(mat_title)
            if not mat:
                print(f"  ⚠️  Skipping item {mat_title}: not found")
                continue
            amount = flt(qty) * flt(rate)
            total_amount += amount
            order_items.append({
                "item_code": mat,
                "quantity": qty,
                "rate": rate,
                "amount": amount,
                "delivery_status": "Delivered" if status == "Delivered" else ("Pending" if status in ("Draft", "Confirmed") else "Partially Delivered"),
            })

        if not order_items:
            continue

        # Set docstatus based on status
        docstatus = 1 if status in ("Confirmed", "Processing", "Shipped", "Delivered") else 0
        # Cancelled orders: status Cancelled, docstatus 2
        if status == "Cancelled":
            docstatus = 2

        discount = flt(total_amount * 0.02) if total_amount > 100000 else 0
        advance = flt(total_amount * 0.1) if pay_status == "Partial" else (total_amount if pay_status == "Completed" else 0)
        net_amount = total_amount - discount
        balance = net_amount - advance

        delivery_address = {
            "Raj Constructions": "25, MG Road, Camp, Pune",
            "Greenfield Developers": "88, Koramangala Industrial Layout, Bangalore",
            "Urban Infrastructure": "Plot 15, Bandra Kurla Complex, Mumbai",
            "Skyline Builders": "12, Jubilee Hills Road 36, Hyderabad",
            "Blueprint Architects": "45, Cathedral Road, Gopalapuram, Chennai",
            "Apex Constructions": "78, Lajpat Nagar, Part 2, Delhi",
            "Nova Interiors": "33, CG Road, Navrangpura, Ahmedabad",
            "Patel & Sons Construction": "1, Adajan Patia, Surat",
        }.get(cust_name, "")

        contact = frappe.db.get_value("Marketplace Customer", customer, "contact_person") or cust_name
        phone = frappe.db.get_value("Marketplace Customer", customer, "phone") or ""

        order = frappe.get_doc({
            "doctype": "Marketplace Order",
            "naming_series": "MORD-.YYYY.-",
            "customer": customer,
            "order_date": order_date,
            "delivery_date": delivery_date,
            "status": status,
            "payment_status": pay_status,
            "payment_method": pay_method,
            "delivery_address": delivery_address,
            "delivery_city": del_city,
            "delivery_contact": contact,
            "delivery_phone": phone,
            "total_amount": total_amount,
            "discount_amount": discount,
            "advance_amount": advance,
            "net_amount": net_amount,
            "balance_amount": balance,
            "items": order_items,
            "notes": f"<p>Demo order for {cust_name}. Created for testing purposes.</p>",
        })
        order.flags.ignore_permissions = True
        order.insert()

        # Set docstatus for submitted/cancelled orders
        if docstatus == 1:
            frappe.db.set_value("Marketplace Order", order.name, "docstatus", 1)
        elif docstatus == 2:
            frappe.db.set_value("Marketplace Order", order.name, "docstatus", 2)

        orders[order.name] = {
            "customer": customer,
            "status": status,
            "delivery_date": delivery_date,
            "order_date": order_date,
        }
        print(f"  ✅ Created order: {order.name} ({status})")

    print(f"✅ Orders: {len(orders)} created\n")
    return orders


# ---------------------------------------------------------------------------
# Step 7 — Customer Enquiries (12)
# ---------------------------------------------------------------------------

def _create_enquiries(customers, materials):
    """Create 12 customer enquiries in various statuses."""
    now = nowdate()

    enquiry_defs = [
        ("Raj Constructions", 30, "Closed", "Ultratech PPC Cement - PPC Grade", 100,
         "Need cement urgently for foundation work at our new project site in Wakad."),
        ("Greenfield Developers", 25, "Quoted", "AAC Lightweight Blocks - AAC Lightweight", 1000,
         "Looking for bulk pricing on AAC blocks for our eco-friendly township project."),
        ("Urban Infrastructure", 20, "Converted to Order", "ACC OPC 53 Grade Cement - OPC 53 Grade", 500,
         "Require high-grade cement for high-rise tower foundation."),
        ("Skyline Builders", 18, "Open", "JSW Fe 550 TMT Steel - Fe 550", 10,
         "Need Fe 550 grade TMT steel for our new luxury apartment project."),
        ("Blueprint Architects", 15, "Quoted", "Birla Gold OPC 43 Grade Cement - OPC 43 Grade", 200,
         "Specifying materials for a new school building project."),
        ("Apex Constructions", 12, "Open", "M Sand for Concrete - Concrete M Sand", 600,
         "Need concrete M sand for ongoing metro rail project."),
        ("Nova Interiors", 10, "Open", "Table Mould Red Bricks - Table Mould", 3000,
         "Require table mould bricks for interior partition walls in commercial project."),
        ("Patel & Sons Construction", 22, "Closed", "Wirecut Red Bricks - Wirecut Bricks", 5000,
         "Price enquiry for bulk wirecut bricks for township project in Surat."),
        ("Raj Constructions", 8, "Open", "M Sand for Plastering - Plastering M Sand", 400,
         "Need plastering M sand for finishing work on 2 residential towers."),
        ("Urban Infrastructure", 6, "Open", "JSW Fe 500D TMT Steel - Fe 500D", 15,
         "Require Fe 500D TMT steel for commercial complex in BKC."),
        ("Greenfield Developers", 14, "Quoted", "Solid Concrete Blocks - Solid Concrete Blocks", 2000,
         "Looking for concrete blocks for boundary walls and landscaping."),
        ("Nova Interiors", 4, "Open", "Birla Gold OPC 43 Grade Cement - OPC 43 Grade", 50,
         "Small quantity needed for interior renovation project."),
    ]

    created = 0
    for cust_name, days_ago, status, mat_title, qty, desc in enquiry_defs:
        customer = customers.get(cust_name)
        material = materials.get(mat_title)
        if not customer:
            continue

        enquiry_date = add_days(now, -days_ago)
        pref_delivery = add_days(enquiry_date, random.randint(15, 45))

        enquiry = frappe.get_doc({
            "doctype": "Customer Enquiry",
            "naming_series": "ENQ-.YYYY.-",
            "customer": customer,
            "contact_number": frappe.db.get_value("Marketplace Customer", customer, "phone") or "",
            "email": frappe.db.get_value("Marketplace Customer", customer, "email") or "",
            "enquiry_date": enquiry_date,
            "status": status,
            "material": material or "",
            "quantity": qty if material else 0,
            "preferred_delivery_date": pref_delivery,
            "delivery_address": frappe.db.get_value("Marketplace Customer", customer, "address") or "",
            "description": f"<p>{desc}</p>",
        })
        enquiry.flags.ignore_permissions = True
        enquiry.insert()
        created += 1

    print(f"✅ Enquiries: {created} created\n")
    return None


# ---------------------------------------------------------------------------
# Step 8 — Purchase Orders (10)
# ---------------------------------------------------------------------------

def _create_purchase_orders(suppliers, materials, orders):
    """Create 10 purchase orders with items in various statuses."""
    now = nowdate()

    po_defs = [
        ("BuildMart Supplies", 30, "Received", "Net 30", [
            ("Ultratech PPC Cement - PPC Grade", 100, 350),
            ("ACC OPC 53 Grade Cement - OPC 53 Grade", 50, 380),
        ]),
        ("SteelKing Distributors", 25, "Received", "Net 45", [
            ("JSW Fe 500D TMT Steel - Fe 500D", 5, 68000),
            ("Tata Tiscon Fe 500 TMT Steel - Fe 500", 8, 65000),
        ]),
        ("Prime Cement Traders", 20, "Partially Received", "Advance Payment", [
            ("Ultratech PPC Cement - PPC Grade", 200, 340),
            ("Birla Gold OPC 43 Grade Cement - OPC 43 Grade", 150, 330),
        ]),
        ("Sand Depot", 18, "Partially Received", "Net 15", [
            ("M Sand for Plastering - Plastering M Sand", 500, 45),
            ("M Sand for Concrete - Concrete M Sand", 400, 52),
        ]),
        ("BrickHouse Bricks", 15, "Submitted", "On Delivery", [
            ("Wirecut Red Bricks - Wirecut Bricks", 5000, 8),
            ("Solid Concrete Blocks - Solid Concrete Blocks", 1000, 35),
        ]),
        ("Metro Constructions Supply", 12, "Submitted", "Net 30", [
            ("JSW Fe 500D TMT Steel - Fe 500D", 3, 67500),
            ("JSW Fe 550 TMT Steel - Fe 550", 2, 71500),
        ]),
        ("Apex Building Materials", 10, "Draft", "Net 30", [
            ("AAC Lightweight Blocks - AAC Lightweight", 800, 53),
            ("Table Mould Red Bricks - Table Mould", 3000, 7.2),
        ]),
        ("TransCon Logistics & Supply", 8, "Draft", "Net 45", [
            ("ACC OPC 53 Grade Cement - OPC 53 Grade", 150, 375),
            ("M Sand for Concrete - Concrete M Sand", 300, 50),
        ]),
        ("BuildMart Supplies", 5, "Draft", "Net 30", [
            ("Wirecut Red Bricks - Wirecut Bricks", 2000, 8.5),
            ("AAC Lightweight Blocks - AAC Lightweight", 400, 55),
        ]),
        ("SteelKing Distributors", 3, "Draft", "On Delivery", [
            ("JSW Fe 550 TMT Steel - Fe 550", 3, 72000),
        ]),
    ]

    purchase_orders = []
    for supp_name, days_ago, status, payment_terms, items in po_defs:
        supplier = suppliers.get(supp_name)
        if not supplier:
            print(f"  ⚠️  Skipping PO for {supp_name}: supplier not found")
            continue

        order_date = add_days(now, -days_ago)
        expected_delivery = add_days(order_date, random.randint(7, 30))

        total_qty = 0
        total_amount = 0
        po_items = []
        for mat_title, qty, rate in items:
            mat = materials.get(mat_title)
            if not mat:
                continue
            amount = flt(qty) * flt(rate)
            total_qty += qty
            total_amount += amount
            received = qty if status == "Received" else (qty * 0.6 if status == "Partially Received" else 0)
            po_items.append({
                "item_code": mat,
                "qty": qty,
                "rate": rate,
                "amount": amount,
                "received_qty": flt(received),
            })

        if not po_items:
            continue

        docstatus = 1 if status in ("Submitted", "Partially Received", "Received") else 0
        discount = flt(total_amount * 0.02) if total_amount > 200000 else 0

        po = frappe.get_doc({
            "doctype": "Purchase Order",
            "naming_series": "PO-.YYYY.-",
            "supplier": supplier,
            "order_date": order_date,
            "expected_delivery_date": expected_delivery,
            "status": status,
            "payment_terms": payment_terms,
            "total_qty": total_qty,
            "total_amount": total_amount,
            "discount_amount": discount,
            "net_amount": total_amount - discount,
            "items": po_items,
        })
        po.flags.ignore_permissions = True
        po.insert()

        if docstatus == 1:
            frappe.db.set_value("Purchase Order", po.name, "docstatus", 1)

        purchase_orders.append(po.name)
        print(f"  ✅ Created PO: {po.name} ({status})")

    print(f"✅ Purchase Orders: {len(purchase_orders)} created\n")
    return purchase_orders


# ---------------------------------------------------------------------------
# Step 9 — Material Requests (10)
# ---------------------------------------------------------------------------

def _create_material_requests(materials):
    """Create 10 material requests with items in various statuses."""
    now = nowdate()

    mr_defs = [
        ("High", "Greenfield Township Project", 30, "Ordered", [
            ("Ultratech PPC Cement - PPC Grade", 200),
            ("M Sand for Concrete - Concrete M Sand", 500),
        ]),
        ("High", "Commercial Tower BKC", 25, "Approved", [
            ("ACC OPC 53 Grade Cement - OPC 53 Grade", 300),
            ("JSW Fe 500D TMT Steel - Fe 500D", 8),
        ]),
        ("Medium", "Residential Complex Wakad", 20, "Ordered", [
            ("Wirecut Red Bricks - Wirecut Bricks", 5000),
            ("M Sand for Plastering - Plastering M Sand", 400),
        ]),
        ("Urgent", "Metro Station Project", 15, "Approved", [
            ("Tata Tiscon Fe 500 TMT Steel - Fe 500", 10),
            ("M Sand for Concrete - Concrete M Sand", 600),
        ]),
        ("Medium", "School Building Chennai", 18, "Partially Ordered", [
            ("Birla Gold OPC 43 Grade Cement - OPC 43 Grade", 150),
            ("Solid Concrete Blocks - Solid Concrete Blocks", 1000),
        ]),
        ("High", "Luxury Apartments Hyderabad", 12, "Approved", [
            ("JSW Fe 550 TMT Steel - Fe 550", 5),
            ("AAC Lightweight Blocks - AAC Lightweight", 800),
        ]),
        ("Low", "Interior Project Ahmedabad", 10, "Draft", [
            ("Table Mould Red Bricks - Table Mould", 2000),
            ("Birla Gold OPC 43 Grade Cement - OPC 43 Grade", 50),
        ]),
        ("Medium", "Township Project Surat", 22, "Approved", [
            ("Wirecut Red Bricks - Wirecut Bricks", 10000),
            ("Ultratech PPC Cement - PPC Grade", 300),
        ]),
        ("High", "Commercial Complex Delhi", 14, "Partially Ordered", [
            ("ACC OPC 53 Grade Cement - OPC 53 Grade", 250),
            ("JSW Fe 500D TMT Steel - Fe 500D", 6),
        ]),
        ("Medium", "Housing Society Repairs", 7, "Draft", [
            ("M Sand for Plastering - Plastering M Sand", 150),
            ("Birla Gold OPC 43 Grade Cement - OPC 43 Grade", 30),
        ]),
    ]

    created = 0
    for priority, project, days_ago, status, items in mr_defs:
        request_date = add_days(now, -days_ago)
        required_by = add_days(now, random.randint(7, 45))

        mr_items = []
        for mat_title, qty in items:
            mat = materials.get(mat_title)
            if not mat:
                continue
            ordered_qty = qty if status == "Ordered" else (qty * 0.5 if status == "Partially Ordered" else 0)
            mr_items.append({
                "item_code": mat,
                "qty": qty,
                "ordered_qty": flt(ordered_qty),
                "required_date": required_by,
            })

        if not mr_items:
            continue

        mr = frappe.get_doc({
            "doctype": "Material Request",
            "naming_series": "MREQ-.YYYY.-",
            "title": f"Material Request - {project}",
            "requested_by": "Administrator",
            "request_date": request_date,
            "required_by_date": required_by,
            "status": status,
            "priority": priority,
            "for_project": project,
            "items": mr_items,
            "notes": f"<p>Material request for {project}. Priority: {priority}.</p>",
        })
        mr.flags.ignore_permissions = True
        mr.insert()
        created += 1

    print(f"✅ Material Requests: {created} created\n")


# ---------------------------------------------------------------------------
# Step 10 — Delivery Schedules (8)
# ---------------------------------------------------------------------------

def _create_delivery_schedules(orders, materials):
    """Create 8 delivery schedules linked to delivered/shipped orders."""
    now = nowdate()

    # Filter orders that have been delivered or shipped
    deliverable_orders = [
        (name, data) for name, data in orders.items()
        if data["status"] in ("Delivered", "Shipped")
    ]

    # Take all deliverable orders for delivery scheduling
    scheduled_data = []
    for i, (order_name, data) in enumerate(deliverable_orders[:6]):
        order_doc = frappe.get_doc("Marketplace Order", order_name)
        item_lines = []
        for item in order_doc.items:
            item_lines.append({
                "item_code": item.item_code,
                "ordered_quantity": item.quantity,
                "delivered_quantity": item.quantity if data["status"] == "Delivered" else flt(item.quantity * 0.6),
                "pending_quantity": 0 if data["status"] == "Delivered" else flt(item.quantity * 0.4),
            })

        status = "Delivered" if data["status"] == "Delivered" else "In Transit"
        days_offset = (getdate(now) - getdate(data["delivery_date"])).days if data["status"] == "Delivered" else -random.randint(2, 5)
        actual_delivery = add_days(now, -abs(days_offset)) if data["status"] == "Delivered" else None

        vehicle_info = {
            "vehicle_number": f"MH 01 AB {1234 + i}",
            "driver_name": ["Rahul Singh", "Mohan Lal", "Suresh Yadav", "Amit Kumar",
                           "Vijay Pawar", "Sunil Joshi", "Ravi Deshmukh", "Prakash Rao"][i],
            "driver_contact": f"99887766{40 + i}",
            "transporter_name": ["Speed Cargo", "RapidTrans", "SafeMove Logistics",
                                "Express Hauliers", "Prime Transport", "CityWide Carriers",
                                "National Movers", "Swift Logistics"][i],
            "freight_charge": random.randint(2000, 15000),
        }

        scheduled_data.append({
            "order": order_name,
            "scheduled_date": add_days(data["delivery_date"], -2),
            "actual_delivery_date": actual_delivery,
            "delivery_status": status,
            "items": item_lines,
            **vehicle_info,
        })

    created = 0
    for sd in scheduled_data:
        ds = frappe.get_doc({
            "doctype": "Delivery Schedule",
            "naming_series": "DEL-.YYYY.-",
            "order": sd["order"],
            "scheduled_date": sd["scheduled_date"],
            "actual_delivery_date": sd.get("actual_delivery_date"),
            "delivery_status": sd["delivery_status"],
            "vehicle_number": sd.get("vehicle_number"),
            "driver_name": sd.get("driver_name"),
            "driver_contact": sd.get("driver_contact"),
            "transporter_name": sd.get("transporter_name"),
            "freight_charge": sd.get("freight_charge"),
            "items": sd["items"],
        })
        ds.flags.ignore_permissions = True
        ds.insert()

        # Submit delivered schedules
        if sd["delivery_status"] == "Delivered":
            frappe.db.set_value("Delivery Schedule", ds.name, "docstatus", 1)

        created += 1
        print(f"  ✅ Created delivery: {ds.name} ({sd['delivery_status']})")

    # Add 4 more deliveries for Confirmed/Processing orders (as Scheduled)
    scheduled_orders = [
        (name, data) for name, data in orders.items()
        if data["status"] in ("Confirmed", "Processing")
    ]
    for i, (order_name, data) in enumerate(scheduled_orders[:4]):
        idx = len(scheduled_data) + i
        order_doc = frappe.get_doc("Marketplace Order", order_name)
        item_lines = []
        for item in order_doc.items:
            item_lines.append({
                "item_code": item.item_code,
                "ordered_quantity": item.quantity,
                "delivered_quantity": 0,
                "pending_quantity": item.quantity,
            })

        ds = frappe.get_doc({
            "doctype": "Delivery Schedule",
            "naming_series": "DEL-.YYYY.-",
            "order": order_name,
            "scheduled_date": add_days(data["delivery_date"], -5),
            "actual_delivery_date": None,
            "delivery_status": "Scheduled",
            "vehicle_number": f"MH 02 CD {5000 + idx}",
            "driver_name": ["Rajiv Kapoor", "Deepak Sharma", "Sanjay Gupta", "Rohit Singh"][i],
            "driver_contact": f"99887777{50 + idx}",
            "transporter_name": ["City Logistics", "Metro Movers", "Prime Haulers", "Star Cargo"][i],
            "freight_charge": random.randint(3000, 12000),
            "items": item_lines,
        })
        ds.flags.ignore_permissions = True
        ds.insert()
        created += 1
        print(f"  ✅ Created delivery: {ds.name} (Scheduled)")

    print(f"✅ Deliveries: {created} created\n")


# ---------------------------------------------------------------------------
# Step 11 — Quality Checks (8)
# ---------------------------------------------------------------------------

def _create_quality_checks(materials, suppliers, orders):
    """Create 8 quality checks with parameters for various materials."""
    now = nowdate()

    qc_defs = [
        ("Ultratech PPC Cement - PPC Grade", "BuildMart Supplies", 30, "Accepted", "QC-001",
         "Rajesh Kumar", [
             ("Fineness (Specific Surface)", "225 m²/kg min", "260 m²/kg", "Pass"),
             ("Setting Time - Initial", "30 min min", "45 min", "Pass"),
             ("Setting Time - Final", "600 min max", "480 min", "Pass"),
             ("Compressive Strength 3 days", "27 N/mm² min", "31 N/mm²", "Pass"),
             ("Compressive Strength 7 days", "37 N/mm² min", "42 N/mm²", "Pass"),
             ("Soundness (Le Chatelier)", "10 mm max", "3 mm", "Pass"),
         ]),
        ("ACC OPC 53 Grade Cement - OPC 53 Grade", "Prime Cement Traders", 25, "Accepted", "QC-002",
         "Rajesh Kumar", [
             ("Fineness (Specific Surface)", "225 m²/kg min", "280 m²/kg", "Pass"),
             ("Setting Time - Initial", "30 min min", "50 min", "Pass"),
             ("Compressive Strength 7 days", "37 N/mm² min", "45 N/mm²", "Pass"),
             ("Compressive Strength 28 days", "53 N/mm² min", "58 N/mm²", "Pass"),
         ]),
        ("JSW Fe 500D TMT Steel - Fe 500D", "SteelKing Distributors", 20, "Accepted", "QC-003",
         "Amit Sharma", [
             ("Yield Strength", "500 N/mm² min", "540 N/mm²", "Pass"),
             ("Tensile Strength", "585 N/mm² min", "620 N/mm²", "Pass"),
             ("Elongation %", "16% min", "20%", "Pass"),
             ("Bend Test (180°)", "No cracks", "No cracks", "Pass"),
             ("Rebend Test", "No cracks", "No cracks", "Pass"),
         ]),
        ("Tata Tiscon Fe 500 TMT Steel - Fe 500", "SteelKing Distributors", 18, "Conditional", "QC-004",
         "Amit Sharma", [
             ("Yield Strength", "500 N/mm² min", "510 N/mm²", "Pass"),
             ("Tensile Strength", "585 N/mm² min", "600 N/mm²", "Pass"),
             ("Elongation %", "14.5% min", "14%", "Fail"),
             ("Bend Test (180°)", "No cracks", "Minor surface crack", "Fail"),
         ]),
        ("M Sand for Concrete - Concrete M Sand", "Sand Depot", 15, "Accepted", "QC-005",
         "Suresh Reddy", [
             ("Sieve Analysis - Zone", "Zone II", "Zone II", "Pass"),
             ("Fineness Modulus", "2.6 - 3.2", "2.9", "Pass"),
             ("Silt Content", "3% max", "1.5%", "Pass"),
             ("Moisture Content", "5% max", "2.8%", "Pass"),
         ]),
        ("Wirecut Red Bricks - Wirecut Bricks", "BrickHouse Bricks", 12, "Accepted", "QC-006",
         "Mohan Das", [
             ("Compressive Strength", "3.5 N/mm² min", "4.2 N/mm²", "Pass"),
             ("Water Absorption", "20% max", "15%", "Pass"),
             ("Efflorescence", "Nil to Slight", "Nil", "Pass"),
             ("Dimensions Tolerance", "±3 mm", "±2 mm", "Pass"),
         ]),
        ("AAC Lightweight Blocks - AAC Lightweight", "BuildMart Supplies", 10, "Rejected", "QC-007",
         "Vikram Patil", [
             ("Dry Density", "550-650 kg/m³", "720 kg/m³", "Fail"),
             ("Compressive Strength", "3.0 N/mm² min", "2.4 N/mm²", "Fail"),
             ("Dimensions", "600x200x200 mm", "598x198x202 mm", "Pass"),
             ("Surface Finish", "Smooth", "Rough surface", "Fail"),
         ]),
        ("M Sand for Plastering - Plastering M Sand", "Sand Depot", 8, "Accepted", "QC-008",
         "Suresh Reddy", [
             ("Fineness Modulus", "1.5 - 2.5", "2.1", "Pass"),
             ("Silt Content", "3% max", "1.2%", "Pass"),
             ("Grain Shape", "Angular", "Sub-angular", "Pass"),
             ("Moisture Content", "5% max", "2.5%", "Pass"),
         ]),
    ]

    created = 0
    for mat_title, supp_name, days_ago, result, lot, inspector, params in qc_defs:
        mat = materials.get(mat_title)
        supplier = suppliers.get(supp_name)
        if not mat:
            continue

        inspection_date = add_days(now, -days_ago)

        qc_params = []
        for param, std_val, meas_val, p_result in params:
            qc_params.append({
                "parameter": param,
                "standard_value": std_val,
                "measured_value": meas_val,
                "result": p_result,
            })

        # Find an order that contains this material if possible
        order_link = ""
        for o_name, o_data in orders.items():
            if o_data.get("status") in ("Delivered", "Shipped"):
                order_doc = frappe.get_doc("Marketplace Order", o_name)
                for item in order_doc.items:
                    if item.item_code == mat:
                        order_link = o_name
                        break
                if order_link:
                    break

        qty_checked = random.randint(50, 500)
        sample = random.randint(5, 25)
        if result == "Accepted":
            qty_accepted = qty_checked
            qty_rejected = 0
        elif result == "Rejected":
            qty_accepted = 0
            qty_rejected = qty_checked
        else:
            qty_accepted = flt(qty_checked * 0.7)
            qty_rejected = flt(qty_checked * 0.3)

        qc = frappe.get_doc({
            "doctype": "Quality Check",
            "naming_series": "QC-.YYYY.-",
            "material": mat,
            "supplier": supplier or "",
            "order": order_link or "",
            "inspection_date": inspection_date,
            "result": result,
            "inspector_name": inspector,
            "lot_number": lot,
            "quantity_checked": qty_checked,
            "quantity_accepted": qty_accepted,
            "quantity_rejected": qty_rejected,
            "sample_size": sample,
            "parameters": qc_params,
            "notes": f"<p>Quality check for {mat_title}. Result: {result}. Lot: {lot}.</p>",
        })
        qc.flags.ignore_permissions = True
        qc.insert()
        created += 1
        print(f"  ✅ Created QC: {qc.name} ({result})")

    # Add 2 more quality checks for remaining materials
    extra_qcs = [
        ("Solid Concrete Blocks - Solid Concrete Blocks", "BrickHouse Bricks", 6, "Pending", "QC-009",
         "Mohan Das", [
             ("Compressive Strength 7 days", "5.0 N/mm² min", "—", ""),
             ("Water Absorption", "10% max", "—", ""),
             ("Dimensions", "400x200x100 mm", "—", ""),
             ("Density", "1800-2200 kg/m³", "—", ""),
         ]),
        ("Birla Gold OPC 43 Grade Cement - OPC 43 Grade", "Prime Cement Traders", 4, "Pending", "QC-010",
         "Rajesh Kumar", [
             ("Fineness (Specific Surface)", "225 m²/kg min", "—", ""),
             ("Setting Time - Initial", "30 min min", "—", ""),
             ("Compressive Strength 7 days", "33 N/mm² min", "—", ""),
             ("Soundness (Le Chatelier)", "10 mm max", "—", ""),
         ]),
    ]

    for mat_title, supp_name, days_ago, result, lot, inspector, params in extra_qcs:
        mat = materials.get(mat_title)
        supplier = suppliers.get(supp_name)
        if not mat:
            continue

        inspection_date = add_days(now, -days_ago)

        qc_params = []
        for param, std_val, meas_val, p_result in params:
            qc_params.append({
                "parameter": param,
                "standard_value": std_val,
                "measured_value": meas_val,
                "result": p_result,
            })

        qc = frappe.get_doc({
            "doctype": "Quality Check",
            "naming_series": "QC-.YYYY.-",
            "material": mat,
            "supplier": supplier or "",
            "inspection_date": inspection_date,
            "result": result,
            "inspector_name": inspector,
            "lot_number": lot,
            "quantity_checked": 0,
            "quantity_accepted": 0,
            "quantity_rejected": 0,
            "sample_size": 0,
            "parameters": qc_params,
            "notes": f"<p>Quality check for {mat_title}. Result: {result}. Lot: {lot}.</p>",
        })
        qc.flags.ignore_permissions = True
        qc.insert()
        created += 1
        print(f"  ✅ Created QC: {qc.name} ({result})")

    print(f"✅ Quality Checks: {created} created\n")


# ---------------------------------------------------------------------------
# Step 12 — Marketplace Settings
# ---------------------------------------------------------------------------

def _setup_marketplace_settings():
    """Configure the Marketplace Settings Single DocType."""
    existing = frappe.db.get_single_value("Marketplace Settings", "upi_id")

    if existing:
        print("⏩ Marketplace Settings already configured\n")
        return

    settings = frappe.get_single("Marketplace Settings")
    settings.upi_id = "constructionmarketplace@upi"
    settings.merchant_name = "Construction Marketplace"
    settings.account_holder = "Construction Marketplace Pvt Ltd"
    settings.bank_name = "HDFC Bank"
    settings.account_number = "50100567890123"
    settings.ifsc_code = "HDFC0001234"
    settings.flags.ignore_permissions = True
    settings.save()
    print("✅ Marketplace Settings configured\n")


# ---------------------------------------------------------------------------
# Step 13 — Link related documents
# ---------------------------------------------------------------------------

def _link_related_docs(purchase_orders, orders):
    """Link some purchase orders to marketplace orders and material requests."""
    # Find delivered orders and map them to POs
    delivered_orders = [
        name for name, data in orders.items()
        if data["status"] == "Delivered"
    ]

    for i, po_name in enumerate(purchase_orders[:3]):
        if i < len(delivered_orders):
            frappe.db.set_value("Purchase Order", po_name, "marketplace_order", delivered_orders[i])

    # Link first PO to a material request
    mr_name = frappe.db.get_value("Material Request", {}, "name")
    if mr_name and purchase_orders:
        frappe.db.set_value("Purchase Order", purchase_orders[0], "material_request", mr_name)

    print("✅ Related documents linked\n")
