# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.naming import make_autoname


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
                    "current_stock": mat["reorder_level"] * 2,
                    "specifications": []
                })
                # Use in_import flag to skip _set_defaults() which can fail
                # when the child table controller module path isn't found
                import_flag = frappe.flags.in_import
                frappe.flags.in_import = True
                doc.insert(ignore_permissions=True)
                frappe.flags.in_import = import_flag
    
    frappe.db.commit()


def _fix_child_table_modules():
    """Fix module assignment for child table doctypes in the database.
    
    On some Frappe installations, child table doctypes may have their
    module field set to 'Core' instead of the correct module. This
    helper updates them so Frappe can find their controllers.
    """
    child_tables = [
        "Material Specification",
        "Order Item",
        "Delivery Item",
        "Quality Check Parameter",
        "Purchase Order Item",
        "Material Request Item"
    ]
    updated = 0
    for ct in child_tables:
        current_module = frappe.db.get_value("DocType", ct, "module")
        if current_module != "Construction Marketplace":
            frappe.db.set_value("DocType", ct, "module", "Construction Marketplace")
            updated += 1
    if updated:
        frappe.db.commit()
        print(f"✅ Fixed module for {updated} child table doctypes")
    else:
        print("✅ All child table doctypes already have correct module")


def create_all_sample_data():
    """
    Create complete sample data for testing the marketplace.
    Run this after app installation:
    bench --site your-site execute construction_marketplace.install.create_all_sample_data
    """
    # Fix child table module paths before creating any data
    _fix_child_table_modules()
    
    # Ensure base data exists
    create_default_categories()
    create_default_grades()
    create_demo_materials()

    # --- Create Suppliers ---
    suppliers = [
        {
            "supplier_name": "BuildMart Supplies",
            "company_name": "BuildMart Pvt Ltd",
            "contact_person": "Ramesh Kumar",
            "email": "ramesh@buildmart.com",
            "phone": "9876543210",
            "city": "Mumbai",
            "state": "Maharashtra",
            "country": "India",
            "is_approved": 1,
            "rating": 4.5
        },
        {
            "supplier_name": "SteelKing Distributors",
            "company_name": "SteelKing Ltd",
            "contact_person": "Amit Singh",
            "email": "amit@steelking.com",
            "phone": "9876543211",
            "city": "Delhi",
            "state": "Delhi",
            "country": "India",
            "is_approved": 1,
            "rating": 4.2
        },
        {
            "supplier_name": "Prime Cement Traders",
            "company_name": "Prime Cement Traders",
            "contact_person": "Suresh Patel",
            "email": "suresh@primecement.com",
            "phone": "9876543212",
            "city": "Ahmedabad",
            "state": "Gujarat",
            "country": "India",
            "is_approved": 1,
            "rating": 4.8
        },
        {
            "supplier_name": "Sand Depot",
            "company_name": "Sand Depot Pvt Ltd",
            "contact_person": "Vikram Reddy",
            "email": "vikram@sanddepot.com",
            "phone": "9876543213",
            "city": "Hyderabad",
            "state": "Telangana",
            "country": "India",
            "is_approved": 1,
            "rating": 4.0
        },
        {
            "supplier_name": "BrickHouse Bricks",
            "company_name": "BrickHouse Bricks Ltd",
            "contact_person": "Mohan Das",
            "email": "mohan@brickhouse.com",
            "phone": "9876543214",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "is_approved": 1,
            "rating": 4.3
        }
    ]
    
    created_suppliers = {}
    for s in suppliers:
        if not frappe.db.exists("Supplier", s["supplier_name"]):
            doc = frappe.get_doc({"doctype": "Supplier", **s})
            doc.insert(ignore_permissions=True)
            created_suppliers[s["supplier_name"]] = doc.name
            print(f"✅ Created Supplier: {s['supplier_name']}")
        else:
            created_suppliers[s["supplier_name"]] = frappe.db.get_value("Supplier", {"supplier_name": s["supplier_name"]}, "name")
            print(f"⏩ Supplier already exists: {s['supplier_name']}")

    # --- Create Customers ---
    customers = [
        {
            "customer_name": "Raj Constructions",
            "company_name": "Raj Constructions Pvt Ltd",
            "customer_type": "Builder",
            "contact_person": "Rajesh Verma",
            "email": "rajesh@rajconstructions.com",
            "phone": "9988776655",
            "city": "Pune",
            "state": "Maharashtra",
            "country": "India",
            "is_verified": 1
        },
        {
            "customer_name": "Greenfield Developers",
            "company_name": "Greenfield Developers",
            "customer_type": "Contractor",
            "contact_person": "Priya Sharma",
            "email": "priya@greenfield.com",
            "phone": "9988776666",
            "city": "Bangalore",
            "state": "Karnataka",
            "country": "India",
            "is_verified": 1
        },
        {
            "customer_name": "Urban Infrastructure",
            "company_name": "Urban Infrastructure Ltd",
            "customer_type": "Builder",
            "contact_person": "Arun Nair",
            "email": "arun@urbaninfra.com",
            "phone": "9988776677",
            "city": "Mumbai",
            "state": "Maharashtra",
            "country": "India",
            "is_verified": 1
        }
    ]
    
    created_customers = {}
    for c in customers:
        if not frappe.db.exists("Marketplace Customer", c["customer_name"]):
            doc = frappe.get_doc({"doctype": "Marketplace Customer", **c})
            doc.insert(ignore_permissions=True)
            created_customers[c["customer_name"]] = doc.name
            print(f"✅ Created Customer: {c['customer_name']}")
        else:
            created_customers[c["customer_name"]] = frappe.db.get_value("Marketplace Customer", {"customer_name": c["customer_name"]}, "name")
            print(f"⏩ Customer already exists: {c['customer_name']}")

    # --- Create Material Prices ---
    price_data = [
        {"supplier": "BuildMart Supplies", "material": "Ultratech PPC Cement - PPC Grade", "price": 350, "uom": "Bag", "min_qty": 10},
        {"supplier": "Prime Cement Traders", "material": "Ultratech PPC Cement - PPC Grade", "price": 340, "uom": "Bag", "min_qty": 20},
        {"supplier": "BuildMart Supplies", "material": "ACC OPC 53 Grade Cement - OPC 53 Grade", "price": 380, "uom": "Bag", "min_qty": 10},
        {"supplier": "Prime Cement Traders", "material": "ACC OPC 53 Grade Cement - OPC 53 Grade", "price": 370, "uom": "Bag", "min_qty": 20},
        {"supplier": "SteelKing Distributors", "material": "JSW Fe 500D TMT Steel - Fe 500D", "price": 68000, "uom": "Ton", "min_qty": 1},
        {"supplier": "SteelKing Distributors", "material": "Tata Tiscon Fe 500 TMT Steel - Fe 500", "price": 65000, "uom": "Ton", "min_qty": 1},
        {"supplier": "Sand Depot", "material": "M Sand for Plastering - Plastering M Sand", "price": 45, "uom": "Cubic Feet", "min_qty": 50},
        {"supplier": "Sand Depot", "material": "M Sand for Concrete - Concrete M Sand", "price": 52, "uom": "Cubic Feet", "min_qty": 50},
        {"supplier": "BrickHouse Bricks", "material": "Wirecut Red Bricks - Wirecut Bricks", "price": 8, "uom": "Pieces", "min_qty": 500},
        {"supplier": "BuildMart Supplies", "material": "AAC Lightweight Blocks - AAC Lightweight", "price": 55, "uom": "Pieces", "min_qty": 100}
    ]

    for p in price_data:
        material_name = frappe.db.get_value("Construction Material", {"title": p["material"]}, "name")
        supplier_name = created_suppliers.get(p["supplier"])
        if material_name and supplier_name:
            title = f"{p['material']} @ {p['supplier']}"
            if not frappe.db.exists("Material Price", {"title": title}):
                doc = frappe.get_doc({
                    "doctype": "Material Price",
                    "title": title,
                    "material": material_name,
                    "supplier": supplier_name,
                    "price_per_unit": p["price"],
                    "unit_of_measure": p["uom"],
                    "minimum_order_qty": p["min_qty"],
                    "is_active": 1
                })
                doc.insert(ignore_permissions=True)
                print(f"✅ Created Price: {p['material']} @ {p['supplier']} = ₹{p['price']}")
        else:
            print(f"⚠️  Skipped price: {p['material']} - material or supplier not found")

    # --- Create Sample Order ---
    customer = created_customers.get("Raj Constructions")
    if customer:
        cement_item = frappe.db.get_value("Construction Material", {"title": "Ultratech PPC Cement - PPC Grade"}, "name")
        steel_item = frappe.db.get_value("Construction Material", {"title": "JSW Fe 500D TMT Steel - Fe 500D"}, "name")
        
        if cement_item and steel_item:
            order_name = make_autoname("MORD-.YYYY.-")
            now = frappe.utils.now()
            today = frappe.utils.nowdate()
            user = frappe.session.user

            frappe.db.sql("""
                INSERT INTO `tabMarketplace Order`
                (name, owner, creation, modified, modified_by, docstatus, idx,
                 naming_series, customer, order_date, status, delivery_city, delivery_state,
                 total_amount, net_amount)
                VALUES
                (%s, %s, %s, %s, %s, 0, 0,
                 'MORD-.YYYY.-', %s, %s, 'Draft', %s, %s,
                 153500, 153500)
            """, (order_name, user, now, now, user,
                   customer, today, "Pune", "Maharashtra"))
            
            # Insert order items directly
            item_idx = 1
            for item_data in [
                (cement_item, "Ultratech PPC Cement - PPC Grade", 50, 350, "Bag", 17500),
                (steel_item, "JSW Fe 500D TMT Steel - Fe 500D", 2, 68000, "Ton", 136000)
            ]:
                child_name = frappe.db.sql("""
                    INSERT INTO `tabOrder Item`
                    (name, owner, creation, modified, modified_by, docstatus, idx,
                     parent, parentfield, parenttype, item_code, material_name, quantity, rate, unit_of_measure, amount)
                    VALUES
                    (%s, %s, %s, %s, %s, 0, %s,
                     %s, 'items', 'Marketplace Order', %s, %s, %s, %s, %s, %s)
                """, (
                    f"{order_name}-{chr(64 + item_idx)}", user, now, now, user, item_idx,
                    order_name, item_data[0], item_data[1], item_data[2], item_data[3], item_data[4], item_data[5]
                ))
                item_idx += 1
            
            print(f"✅ Created Sample Order: {order_name} (₹153500)")

    # --- Create Sample Purchase Order ---
    buildmart = created_suppliers.get("BuildMart Supplies")
    if buildmart:
        cement_item = frappe.db.get_value("Construction Material", {"title": "Ultratech PPC Cement - PPC Grade"}, "name")
        sand_item = frappe.db.get_value("Construction Material", {"title": "M Sand for Plastering - Plastering M Sand"}, "name")
        
        if cement_item and sand_item:
            po_name = make_autoname("PO-.YYYY.-")
            now = frappe.utils.now()
            today = frappe.utils.nowdate()
            user = frappe.session.user

            frappe.db.sql("""
                INSERT INTO `tabPurchase Order`
                (name, owner, creation, modified, modified_by, docstatus, idx,
                 naming_series, supplier, order_date, status, payment_terms,
                 total_qty, total_amount, net_amount)
                VALUES
                (%s, %s, %s, %s, %s, 0, 0,
                 'PO-.YYYY.-', %s, %s, 'Submitted', 'Net 30',
                 300, 42400, 42400)
            """, (po_name, user, now, now, user,
                   buildmart, today))
            
            # Insert PO items directly
            item_idx = 1
            for item_data in [
                (cement_item, "Ultratech PPC Cement - PPC Grade", "Bag", 100, 340, 34000),
                (sand_item, "M Sand for Plastering - Plastering M Sand", "Cubic Feet", 200, 42, 8400)
            ]:
                frappe.db.sql("""
                    INSERT INTO `tabPurchase Order Item`
                    (name, owner, creation, modified, modified_by, docstatus, idx,
                     parent, parentfield, parenttype, item_code, material_name, unit_of_measure, qty, rate, amount)
                    VALUES
                    (%s, %s, %s, %s, %s, 0, %s,
                     %s, 'items', 'Purchase Order', %s, %s, %s, %s, %s, %s)
                """, (
                    f"{po_name}-{chr(64 + item_idx)}", user, now, now, user, item_idx,
                    po_name, item_data[0], item_data[1], item_data[2], item_data[3], item_data[4], item_data[5]
                ))
                item_idx += 1
            
            print(f"✅ Created Sample Purchase Order: {po_name} (₹42400)")
    
    # --- Create Sample Material Request ---
    steel_item = frappe.db.get_value("Construction Material", {"title": "JSW Fe 500D TMT Steel - Fe 500D"}, "name")
    brick_item = frappe.db.get_value("Construction Material", {"title": "Wirecut Red Bricks - Wirecut Bricks"}, "name")
    
    if steel_item and brick_item:
        mr_name = make_autoname("MREQ-.YYYY.-")
        now = frappe.utils.now()
        today = frappe.utils.nowdate()
        required_by = frappe.utils.add_days(today, 15)
        user = frappe.session.user

        frappe.db.sql("""
            INSERT INTO `tabMaterial Request`
            (name, owner, creation, modified, modified_by, docstatus, idx,
             naming_series, requested_by, request_date, required_by_date, status, priority, for_project)
            VALUES
            (%s, %s, %s, %s, %s, 0, 0,
             'MREQ-.YYYY.-', %s, %s, %s, 'Approved', 'High', 'Greenfield Township Project')
        """, (mr_name, user, now, now, user,
               user, today, required_by))
        
        # Insert MR items directly
        item_idx = 1
        for item_data in [
            (steel_item, "JSW Fe 500D TMT Steel - Fe 500D", "Ton", 5, frappe.utils.add_days(today, 10)),
            (brick_item, "Wirecut Red Bricks - Wirecut Bricks", "Pieces", 5000, frappe.utils.add_days(today, 20))
        ]:
            frappe.db.sql("""
                INSERT INTO `tabMaterial Request Item`
                (name, owner, creation, modified, modified_by, docstatus, idx,
                 parent, parentfield, parenttype, item_code, material_name, unit_of_measure, qty, required_date)
                VALUES
                (%s, %s, %s, %s, %s, 0, %s,
                 %s, 'items', 'Material Request', %s, %s, %s, %s, %s)
            """, (
                f"{mr_name}-{chr(64 + item_idx)}", user, now, now, user, item_idx,
                mr_name, item_data[0], item_data[1], item_data[2], item_data[3], item_data[4]
            ))
            item_idx += 1
        
        print(f"✅ Created Sample Material Request: {mr_name}")

    frappe.db.commit()
    print("\n" + "=" * 50)
    print("🎉 ALL SAMPLE DATA CREATED SUCCESSFULLY!")
    print("=" * 50)
    print("📦 Materials: 8 demo materials")
    print("🏭 Suppliers: 5 suppliers")
    print("👥 Customers: 3 customers")
    print("💰 Prices: 10 price records")
    print("📋 Orders: 1 sample order with 2 items")
    print("📄 Purchase Orders: 1 sample PO with 2 items")
    print("📋 Material Requests: 1 sample MR with 2 items")
