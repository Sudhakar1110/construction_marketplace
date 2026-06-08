# Standard Operating Procedure (SOP)
## Construction Marketplace — Frappe v15 / ERPNext v15

**Document Version:** 1.0  
**App Version:** 0.1.0  
**Last Updated:** June 2026  
**App Repository:** [github.com/Sudhakar1110/construction_marketplace](https://github.com/Sudhakar1110/construction_marketplace)

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Architecture](#2-system-architecture)
3. [Installation & Setup](#3-installation--setup)
4. [Configuration](#4-configuration)
5. [User Roles & Permissions](#5-user-roles--permissions)
6. [Daily Operations](#6-daily-operations)
7. [Website & Customer Portal](#7-website--customer-portal)
8. [Dashboard & Workspace](#8-dashboard--workspace)
9. [Scheduled Tasks](#9-scheduled-tasks)
10. [Backup & Recovery](#10-backup--recovery)
11. [Deployment](#11-deployment)
12. [Troubleshooting](#12-troubleshooting)
13. [Maintenance](#13-maintenance)
14. [Appendix](#14-appendix)

---

## 1. Introduction

### 1.1 Purpose
This Standard Operating Procedure (SOP) document provides comprehensive guidelines for the installation, configuration, operation, and maintenance of the **Construction Marketplace** application built on Frappe Framework v15+ and ERPNext v15+.

### 1.2 Scope
This SOP covers all operational aspects including system administration, daily operations, user management, data management, troubleshooting, and disaster recovery for the Construction Marketplace platform.

### 1.3 Application Overview
The Construction Marketplace is a comprehensive marketplace solution for construction materials, inspired by platforms like Buildmaadi.com. It enables suppliers to list construction materials (Cement, TMT Steel, M Sand, Bricks, Blocks, etc.) and customers to browse, enquire, and place orders seamlessly.

### 1.4 Key Features
- **Product Management**: Material categories, grades, specifications, inventory tracking
- **Supplier Management**: Registration, approval, ratings, pricing
- **Customer Management**: Registration, verification, order history
- **Order Management**: Enquiries, quotations, order workflow
- **Delivery Management**: Scheduling, tracking, driver assignment
- **Quality Management**: Inspections, parameter checks, acceptance workflow
- **Reports**: Stock reports, sales analysis, supplier performance
- **Customer Dashboard**: Orders, quotations, wishlist, cart, profile
- **Public Website**: Homepage, catalog, material detail pages, customer portal

---

## 2. System Architecture

### 2.1 Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | Frappe v15+ |
| ERP | ERPNext v15+ (optional) |
| Backend | Python 3.10+ |
| Database | MariaDB 10.6+ |
| Frontend | JavaScript, jQuery, Bootstrap 5 |
| Web Server | Nginx + Gunicorn (via Bench) |
| Cache | Redis |
| Task Queue | Redis Queue (RQ) |
| Search | Frappe Search (built-in) |

### 2.2 Application Structure

```
construction_marketplace/
├── config/                           # Module configuration
│   ├── __init__.py
│   └── desktop.py                    # Module definition for desk
├── construction_marketplace/         # Main app package
│   ├── api.py                        # REST API endpoints
│   ├── tasks.py                      # Scheduled task handlers
│   ├── utils.py                      # Utility functions
│   ├── hooks.py                      # App hooks & configuration
│   ├── modules.txt                   # Module registration
│   ├── install.py                    # Installation scripts
│   ├── patches.txt                   # Patch documentation
│   ├── doctype/                      # All doctype definitions
│   │   ├── construction_material/
│   │   ├── customer_enquiry/
│   │   ├── delivery_schedule/
│   │   ├── marketplace_customer/
│   │   ├── marketplace_order/
│   │   ├── material_category/
│   │   ├── material_grade/
│   │   ├── material_price/
│   │   ├── material_request/
│   │   ├── purchase_order/
│   │   ├── quality_check/
│   │   └── supplier/
│   ├── report/                       # Custom reports
│   │   ├── material_stock_report/
│   │   ├── sales_analysis_report/
│   │   └── supplier_performance_report/
│   ├── notification/                 # System notifications
│   │   ├── delivery_alert.json
│   │   ├── low_stock_alert.json
│   │   └── new_order_alert.json
│   ├── workspace/                    # Desk workspace
│   │   └── construction_marketplace/
│   └── www/                          # Public website pages
│       ├── index.html                # Homepage
│       ├── materials.html            # Catalog page
│       ├── material-view.html        # Material detail page
│       ├── dashboard.html            # Customer dashboard
│       ├── checkout.html             # Checkout page
│       └── ...                       # Other website pages
├── public/                           # Static assets
│   ├── css/
│   │   └── construction_marketplace.bundle.css
│   └── js/
│       └── construction_marketplace.bundle.js
├── __init__.py
├── hooks.py
├── modules.txt
├── setup.py
├── requirements.txt
└── pyproject.toml
```

### 2.3 Doctypes Overview

| Doctype | Type | Purpose |
|---------|------|---------|
| Material Category | Master | Categories (Cement, Steel, Sand, etc.) |
| Material Grade | Master | Grades/variants within categories (OPC 53, Fe 500) |
| Construction Material | Master | Product catalog with specs and inventory |
| Supplier | Master | Vendor/supplier information and ratings |
| Marketplace Customer | Master | Buyer/customer information |
| Marketplace Order | Transaction | Customer orders with items |
| Customer Enquiry | Transaction | Inquiries and price quotations |
| Material Price | Transaction | Pricing per material per supplier |
| Delivery Schedule | Transaction | Delivery tracking and scheduling |
| Quality Check | Transaction | Material quality inspection |
| Purchase Order | Transaction | Procurement orders to suppliers |
| Material Request | Transaction | Internal material requisitions |
| Marketplace Settings | Single (Settings) | Payment configuration (UPI ID, bank details) |

### 2.4 Core Workflows

**Order Lifecycle:**
```
Draft → Confirmed → Processing → Shipped → Delivered → Cancelled
```

**Enquiry Lifecycle:**
```
Open → Quoted → Converted to Order → Closed
```

**Delivery Lifecycle:**
```
Scheduled → In Transit → Delivered → Cancelled
```

**Payment States:**
```
Pending → Partially Paid → Paid → Refunded
```

---

## 3. Installation & Setup

### 3.1 Prerequisites

- Frappe Bench installed and configured
- Frappe Framework v15+
- Python 3.10+
- MariaDB 10.6+
- Node.js 18+ (for building assets)

### 3.2 Installation Procedure

**Step 1:** Get the app from the repository
```bash
cd ~/frappe-bench
bench get-app https://github.com/Sudhakar1110/construction_marketplace.git
```

**Step 2:** Install on your site
```bash
bench --site your-site.com install-app construction_marketplace
```

**Step 3:** Build frontend assets
```bash
bench build
```

**Step 4:** Verify installation
```bash
bench --site your-site.com console
```

In the console, run:
```python
import frappe
frappe.db.exists("Module Def", "Construction Marketplace")
# Should return: 'Construction Marketplace'
```

**Step 5:** (Optional) Create sample data for testing
```bash
bench --site your-site.com execute construction_marketplace.install.create_all_sample_data
```

### 3.3 Post-Installation Checklist

| Check | Command / Action | Expected Result |
|-------|-----------------|-----------------|
| Module exists | `bench console` → check Module Def | Module "Construction Marketplace" exists |
| Roles created | Go to Desk → Role list | Construction Manager, Supplier, Customer exist |
| Default categories | Check Material Category list | 7 categories (Cement, Steel, Sand, etc.) |
| Default grades | Check Material Grade list | 17 grades across categories |
| Workspace visible | Visit `/app` after login | Construction Marketplace appears in sidebar |
| Website accessible | Visit `https://your-site.com` | Homepage loads with featured materials |
| JS/CSS loaded | Check browser console | No 404 errors for bundle files |

### 3.4 Demo Data

After installation, create complete sample data:
```bash
bench --site your-site.com execute construction_marketplace.install.create_all_sample_data
```

This creates:
- 8 demo materials (Ultratech Cement, JSW Steel, etc.)
- 5 suppliers (BuildMart, SteelKing, Prime Cement, etc.)
- 3 customers (Raj Constructions, Greenfield Developers, etc.)
- 10 material price records
- 1 sample order (add items via UI)
- 1 sample purchase order (add items via UI)
- 1 sample material request (add items via UI)

---

## 4. Configuration

### 4.1 Material Categories

Navigate to: **Construction Marketplace → Catalog → Material Categories**

1. Click **+ Add Material Category**
2. Enter:
   - **Title**: e.g., "Cement"
   - **Description**: Brief description of the category
   - **Category Image**: (Optional) Upload an image
   - **Is Active**: Check to make visible on the website
3. **Save**

**Pre-seeded categories**: Cement, TMT Steel, M Sand, Bricks, Blocks, Jelly Stones, Other Materials

### 4.2 Material Grades

Navigate to: **Construction Marketplace → Catalog → Material Grades**

1. Click **+ Add Material Grade**
2. Enter:
   - **Grade Name**: e.g., "OPC 53 Grade"
   - **Material Category**: Select the parent category
   - **Description**: e.g., "Ordinary Portland Cement - 53 Grade"
   - **Is Active**: Check to enable
3. **Save**

### 4.3 Construction Materials

Navigate to: **Construction Marketplace → Catalog → Construction Materials**

1. Click **+ Add Construction Material**
2. Fill in:
   - **Material Name**: e.g., "Ultratech PPC Cement"
   - **Category**: Select from Material Category
   - **Grade**: Select from Material Grade
   - **Brand**: e.g., "Ultratech"
   - **Unit of Measure**: Bag, Ton, Cubic Feet, Pieces, etc.
   - **Current Stock**: Initial inventory count
   - **Reorder Level**: Minimum stock threshold
   - **Description**: Detailed description
   - **Image**: Product image
   - **Specifications**: Child table for technical specs (optional)
   - **Is Active**: Check to publish on website
3. **Save**

**Note:** For website display, ensure:
- `Is Active` is checked
- `Route` field is auto-generated (or run `generate_material_routes`)

### 4.4 Marketplace Settings

Navigate to: **Construction Marketplace → Configuration → Marketplace Settings**

This is a **Single DocType** — there is only one record. Configure:
- **UPI ID**: e.g., "merchant@upi"
- **Bank Name**: e.g., "State Bank of India"
- **Account Number**: Bank account for payments
- **IFSC Code**: Bank IFSC code
- **Default Payment Terms**: e.g., "Advance", "Net 30"

### 4.5 Suppliers

Navigate to: **Construction Marketplace → Catalog → Suppliers**

1. Click **+ Add Supplier**
2. Enter:
   - **Supplier Name**: Company or individual name
   - **Contact Person**: Primary contact
   - **Email**: Contact email address
   - **Phone**: Contact phone number
   - **City, State, Country**: Location details
   - **Is Approved**: Check to enable order placement
   - **Rating**: Supplier rating (1-5)
3. **Save**

### 4.6 Material Prices

Navigate to: **Construction Marketplace → Catalog → Material Prices**

1. Click **+ Add Material Price**
2. Enter:
   - **Material**: Select from Construction Materials
   - **Supplier**: Select from Suppliers
   - **Price Per Unit**: Unit price
   - **Unit of Measure**: Must match the material's UOM
   - **Minimum Order Qty**: Minimum purchase quantity
   - **Currency**: Default INR
   - **Effective From/To**: Price validity period
   - **Is Active**: Check to make available
3. **Save**

### 4.7 Marketplace Customers

Navigate to: **Construction Marketplace → Catalog → Marketplace Customers**

Customer records can be:
- Created manually by admins
- Auto-created when users register on the website

Key fields:
- **Customer Name**: Individual or company name
- **Customer Type**: Individual, Contractor, Builder, Business
- **Contact Person**: Primary contact
- **Email, Phone**: Contact details
- **Address**: Delivery address
- **Is Verified**: Check if identity is verified

---

## 5. User Roles & Permissions

### 5.1 Roles

| Role | Desk Access | Home Page | Description |
|------|-------------|-----------|-------------|
| Construction Manager | Yes | `/app/construction-marketplace` | Full management access |
| Supplier | Yes | `/app/construction-marketplace` | Manage their own materials & orders |
| Customer | Yes | `/app/construction-marketplace` | View their own orders & profile |
| System Manager | Yes (built-in) | — | Full administrative access |

### 5.2 Role Permissions

**Construction Manager:**
- Full CRUD access to all doctypes
- Can view all orders, customers, and suppliers
- Can approve suppliers and verify customers
- Can create purchase orders and material requests

**Supplier:**
- Can view and manage their own profile
- Can create and manage their material prices
- Can view orders assigned to them
- Cannot access other suppliers' data

**Customer:**
- Can view and manage their own profile
- Can place orders and enquiries
- Can view their own order history
- Cannot access other customers' data

**System Manager:**
- Full system-level access
- Can manage roles, permissions, and users
- Can access System Settings and customization tools

### 5.3 Assigning Roles to Users

1. Go to **Users** list in the Desk
2. Open the user record
3. Scroll to **Roles** section
4. Click **+ Add Row**
5. Select the appropriate role (Construction Manager, Supplier, Customer)
6. **Save**

### 5.4 Permission Query Conditions

The app implements dynamic row-level permissions:

- **Marketplace Order**: 
  - System Manager / Construction Manager / Supplier: Full access
  - Other users: Only orders they own

- **Customer Enquiry**:
  - System Manager / Construction Manager: Full access
  - Other users: Only enquiries they own

---

## 6. Daily Operations

### 6.1 Order Processing Workflow

**Step 1 — Review New Orders**
1. Navigate to **Construction Marketplace → Orders & Procurement → Marketplace Orders**
2. Filter by status "Draft" or "Confirmed"
3. Review order details, items, and customer information

**Step 2 — Confirm & Process**
1. Open the order
2. Verify items, quantities, and pricing
3. Update status to **Confirmed**
4. Submit the document

**Step 3 — Create Delivery Schedule**
1. Navigate to **Construction Marketplace → Logistics & Quality → Delivery Schedules**
2. Click **+ Add Delivery Schedule**
3. Link to the Marketplace Order
4. Set delivery date, vehicle, and driver details
5. **Save** and **Submit**

**Step 4 — Ship & Deliver**
1. When goods are dispatched, update Delivery Schedule to "In Transit"
2. On delivery completion, update to "Delivered"
3. Update Marketplace Order status to "Delivered"

### 6.2 Handling Customer Enquiries

1. Navigate to **Construction Marketplace → Orders & Procurement → Customer Enquiries**
2. Review open enquiries
3. Contact the customer with pricing and availability
4. Update status to **Quoted**
5. If customer accepts, convert to order (automatic or manual)
6. Update status to **Converted to Order** or **Closed**

### 6.3 Quality Checks

1. Navigate to **Construction Marketplace → Logistics & Quality → Quality Checks**
2. Click **+ Add Quality Check**
3. Link to the Delivery Schedule
4. Add quality parameters (strength, dimensions, visual inspection, etc.)
5. Record results for each parameter
6. Set overall status to **Accepted** or **Rejected**
7. **Save** and **Submit**

### 6.4 Managing Purchase Orders

1. Navigate to **Construction Marketplace → Orders & Procurement → Purchase Orders**
2. Click **+ Add Purchase Order**
3. Select **Supplier**
4. Add items with quantities and rates
5. **Save** → **Submit** → **Order** (to confirm)

### 6.5 Material Requests

1. Navigate to **Construction Marketplace → Orders & Procurement → Material Requests**
2. Click **+ Add Material Request**
3. Select requested materials and quantities
4. Set priority (Low, Medium, High, Urgent)
5. **Save** → **Submit**

### 6.6 Running Reports

Navigate to **Construction Marketplace → Reports** section:

| Report | Purpose | How to Use |
|--------|---------|------------|
| Material Stock Report | View current inventory levels | Filter by category or material |
| Sales Analysis Report | Analyze sales trends and revenue | Filter by date range |
| Supplier Performance Report | Evaluate supplier metrics | Filter by supplier or date |

---

## 7. Website & Customer Portal

### 7.1 Public Pages

| URL | Page | Description |
|-----|------|-------------|
| `/` | Homepage | Hero section, featured materials, categories |
| `/materials` | Catalog | All materials with search & filter |
| `/materials/{route}` | Material Detail | Full details, prices, add to cart |
| `/checkout` | Checkout | Cart review, address, payment |
| `/dashboard` | Customer Dashboard | Orders, quotations, cart, wishlist, profile |
| `/request-quote` | Quote Request | Submit material enquiry |
| `/marketplace` | Marketplace | Overview page |

### 7.2 Customer Dashboard Tabs

| Tab | Content |
|-----|---------|
| **My Orders** | Order history with status, payment details, amount |
| **My Quotations** | Enquiry/quote requests and their status |
| **My Cart** | Saved items with quantities, ready for checkout |
| **My Wishlist** | Saved materials for future reference |
| **Profile** | Account details, address, contact info |

### 7.3 Cart Functionality

- Items persist via **Redis cache** (session-based)
- Cart badge updates in navbar in real-time
- Cart-updated events trigger refresh across pages
- Items can be added from catalog, detail page, and wishlist

### 7.4 Wishlist Functionality

- Items saved via **Redis cache** (session-based)
- Heart icon toggle on all material cards
- Dashboard wishlist tab for full management
- Add to cart directly from wishlist

### 7.5 Website Configuration

Key settings in `hooks.py`:
```python
website_context = {
    "favicon": "/assets/construction_marketplace/images/favicon.png",
    "navbar_search": True,
    "navbar_search_placeholder": "Search materials, suppliers...",
    "hide_login": 0,
}
```

---

## 8. Dashboard & Workspace

### 8.1 Desk Workspace

The workspace is organized into 5 card sections:

| Section | Links |
|---------|-------|
| **Catalog** | Material Categories, Material Grades, Construction Materials, Suppliers, Marketplace Customers, Material Prices |
| **Orders & Procurement** | Marketplace Orders, Customer Enquiries, Purchase Orders, Material Requests |
| **Logistics & Quality** | Delivery Schedules, Quality Checks |
| **Reports** | Material Stock Report, Sales Analysis Report, Supplier Performance Report |
| **Configuration** | Marketplace Settings |

### 8.2 Workspace Shortcuts

| Shortcut | Type | Description |
|----------|------|-------------|
| Marketplace Orders | DocType | Count of active orders |
| Construction Materials | DocType | Count of listed materials |
| Suppliers | DocType | Count of registered suppliers |
| Customer Enquiries | DocType | Count of open enquiries |
| Delivery Schedules | DocType | Quick access to deliveries |
| Quality Checks | DocType | Quick access to inspections |
| Purchase Orders | DocType | Quick access to POs |
| Material Requests | DocType | Quick access to requests |

### 8.3 Navbar Additions

- **Cart Icon** (shopping cart with count badge) — all pages
- **My Account Dropdown** — logged-in users only
  - Dashboard Home
  - My Orders
  - Wishlist
  - Cart
  - My Profile
  - Logout

---

## 9. Scheduled Tasks

### 9.1 Daily Tasks (Every 24 hours)

**Low Stock Alert (`send_low_stock_alerts`)**
- Checks all Construction Materials with `is_active = 1`
- Compares `current_stock` against `reorder_level`
- Sends email alerts to all Construction Managers
- Trigger: `daily` scheduler

**Order Status Update (`update_order_statuses`)**
- Checks for overdue Marketplace Orders
- Logs errors for orders past delivery date
- Trigger: `daily_long` scheduler

### 9.2 Managing Scheduled Tasks

View scheduled tasks in Frappe Desk:
1. Go to **System Settings → Scheduled Job Type**
2. Search for "construction_marketplace"
3. View or modify schedule as needed

Manual execution:
```bash
bench --site your-site.com execute construction_marketplace.construction_marketplace.tasks.send_low_stock_alerts
```

### 9.3 Notifications

Pre-configured system notifications:

| Notification | Event | Recipients |
|-------------|-------|------------|
| New Order Alert | New Marketplace Order | Construction Manager role |
| Delivery Alert | Delivery Schedule updates | Construction Manager role |
| Low Stock Alert | Stock below reorder level | Construction Manager role |

---

## 10. Backup & Recovery

### 10.1 Database Backup

**Automatic (via Bench cron):**
```bash
# Check backup schedule
bench schedule
```

**Manual backup:**
```bash
# Full site backup
bench --site your-site.com backup

# Backup with files
bench --site your-site.com backup --with-files

# Backup to specific path
bench --site your-site.com backup --backup-path /path/to/backups
```

### 10.2 App Code Backup

The application code is version-controlled via Git:
```bash
cd ~/frappe-bench/apps/construction_marketplace
git status
git log --oneline -5
```

### 10.3 Recovery Procedure

**Restore from backup:**
```bash
# List available backups
bench --site your-site.com list-backups

# Restore site
bench --site your-site.com restore /path/to/backup/file.gz

# Restore with files
bench --site your-site.com restore /path/to/backup/file.gz --with-public-files
```

### 10.4 Disaster Recovery Steps

1. **Assess the situation**: Identify what failed (database, code, server)
2. **Restore database** from the latest backup
3. **Verify app code** is at the correct version (`git log`)
4. **Run migration**: `bench --site your-site.com migrate`
5. **Clear cache**: `bench --site your-site.com clear-cache`
6. **Restart services**: `sudo supervisorctl restart all`
7. **Verify**: Check workspace loads, website works, data is intact

---

## 11. Deployment

### 11.1 Standard Deployment Procedure

```bash
# Step 1: Pull latest code
cd ~/frappe-bench/apps/construction_marketplace
git pull origin main

# Step 2: Update requirements if changed
cd ~/frappe-bench
pip install -e apps/construction_marketplace

# Step 3: Build assets if frontend changed
bench build --app construction_marketplace

# Step 4: Run database migration
bench --site your-site.com migrate

# Step 5: Clear cache
bench --site your-site.com clear-cache

# Step 6: Restart services
sudo supervisorctl restart all

# Or for production with individual services:
sudo supervisorctl restart frappe-web:
sudo supervisorctl restart frappe-worker:
sudo supervisorctl restart frappe-schedule:
```

### 11.2 Quick Deploy Script

Create `deploy.sh` in the project root:
```bash
#!/bin/bash
# Deployment script for Construction Marketplace
set -e

SITE="your-site.com"
APP="construction_marketplace"

echo "🚀 Deploying $APP to $SITE..."
cd ~/frappe-bench

# Pull code
echo "📥 Pulling latest code..."
cd apps/$APP && git pull origin main && cd ..

# Build assets
echo "🔨 Building assets..."
bench build --app $APP

# Migrate
echo "🗄️  Running migrations..."
bench --site $SITE migrate

# Clear cache
echo "🧹 Clearing cache..."
bench --site $SITE clear-cache

# Restart
echo "🔄 Restarting services..."
sudo supervisorctl restart frappe-web: frappe-worker: frappe-schedule:

echo "✅ Deployment complete!"
```

### 11.3 Deployment Checklist

| Item | Command |
|------|---------|
| Pull latest code | `git pull origin main` |
| Build assets | `bench build --app construction_marketplace` |
| Run migrations | `bench --site {site} migrate` |
| Clear cache | `bench --site {site} clear-cache` |
| Restart services | `sudo supervisorctl restart all` |
| Verify workspace | Visit `/app` — check workspace appears |
| Verify website | Visit homepage — check materials load |
| Check console | Browser dev tools — no JS/CSS 404 errors |

---

## 12. Troubleshooting

### 12.1 Workspace Not Appearing

| Symptom | Cause | Solution |
|---------|-------|----------|
| Construction Marketplace not in sidebar | `is_standard: 1` missing from JSON | Run `bench migrate` to sync |
| Workspace appears but links broken | Module not registered | Check `modules.txt` exists |
| Workspace only visible to Admin | Missing roles in JSON | Add roles array to workspace JSON |

**Step-by-step fix:**
```bash
cd ~/frappe-bench/apps/construction_marketplace
git pull origin main
bench --site your-site.com migrate
bench --site your-site.com clear-cache
sudo supervisorctl restart frappe-web:
```

**Manual verification:**
```bash
bench --site your-site.com console
```

```python
# In console:
frappe.db.exists("Module Def", "Construction Marketplace")
# If None: run bench install-app to create module

frappe.db.exists("Workspace", "Construction Marketplace")
# If None: run bench migrate to sync
```

### 12.2 Website Pages Not Loading

| Symptom | Cause | Solution |
|---------|-------|----------|
| 404 on homepage | Web pages not found | Verify www/ files exist, check hooks.py |
| CSS/JS not loading | Assets not built | Run `bench build` |
| 500 error on page load | Python error | Check `bench --site {site} console --log` |

**Fix:**
```bash
bench build --app construction_marketplace
bench --site your-site.com clear-cache
sudo supervisorctl restart frappe-web:
```

### 12.3 Cart/Wishlist Not Working

| Symptom | Cause | Solution |
|---------|-------|----------|
| Cart count shows 0 | Redis not saving session | Check Redis connection: `bench redis` |
| Items disappear on refresh | Session not persisting | Check Redis configuration |
| Cart API returns error | API endpoint error | Check `api.py` for syntax errors |

**Fix:**
```bash
# Restart Redis
sudo systemctl restart redis-server

# Or check Redis connectivity
bench --site your-site.com console
```

```python
# In console:
from frappe.utils.redis_wrapper import RedisWrapper
cache = frappe.cache()
cache.set_value("test_key", "test_value")
cache.get_value("test_key")
# Should return "test_value"
```

### 12.4 Permission Errors

| Symptom | Cause | Solution |
|---------|-------|----------|
| "Not permitted" on order view | Missing role assignment | Assign correct role in User record |
| Can't see own orders | Permission query issue | Check `get_permission_query_conditions` in doctype controller |
| Supplier sees all orders | Permission bug | Check `has_permission` function |

### 12.5 Migration Failures

| Symptom | Cause | Solution |
|---------|-------|----------|
| Migration fails with foreign key error | Missing doctype | Install app fresh, then restore data |
| "Table not found" error | Migration order issue | Run `bench --site {site} migrate --force` |
| Patch failure | Broken patch | Check `patches.txt` for syntax errors |

### 12.6 Common Error Codes

| Error | Message | Resolution |
|-------|---------|------------|
| DoesNotExistError | Module {name} not found | Check `modules.txt` and reinstall |
| PermissionError | Not permitted | Check role assignment |
| ValidationError | Invalid field value | Check field data type and constraints |
| LinkValidationError | Invalid link reference | Ensure referenced doctype record exists |

### 12.7 Checking Error Logs

```bash
# View recent errors
bench --site your-site.com console
```

```python
# In console:
frappe.log_error(title="Test", message="Checking error logging")
frappe.get_logs()
```

Or check the **Error Log** doctype in the Desk:
- Navigate to **System → Logs → Error Log**

### 12.8 Clearing Cache

```bash
# Clear all cache for a site
bench --site your-site.com clear-cache

# Clear specific cache
bench --site your-site.com console
```

```python
# In console:
frappe.clear_cache()
frappe.cache().flushall()
```

---

## 13. Maintenance

### 13.1 Routine Maintenance Schedule

| Frequency | Task | Command |
|-----------|------|---------|
| Daily | Check scheduled tasks ran | Monitor Error Log |
| Weekly | Review backup status | `bench --site {site} list-backups` |
| Monthly | Run database optimization | `bench --site {site} optimize` |
| Monthly | Update app (if new version) | See deployment procedure |
| Quarterly | Full DR test | Practice restore on staging site |

### 13.2 Database Maintenance

```bash
# Check database size
bench --site your-site.com console
```

```python
# In console:
frappe.db.sql("SELECT COUNT(*) FROM `tabMarketplace Order`")
frappe.db.sql("SELECT table_schema AS 'Database', SUM(data_length + index_length) / 1024 / 1024 AS 'Size (MB)' FROM information_schema.tables WHERE table_schema = DATABASE() GROUP BY table_schema")
```

### 13.3 Performance Monitoring

Watch for:
- Slow page loads → Check for missing indexes
- Redis memory usage → Monitor with `redis-cli info memory`
- Queue backlog → `bench --site {site} console` → check RQ queues
- Database slow queries → Enable slow query log in MariaDB

### 13.4 Version Upgrades

When upgrading the app:
```bash
# 1. Backup first
bench --site your-site.com backup

# 2. Pull new version
cd apps/construction_marketplace && git pull origin main

# 3. Check for new requirements
cd ~/frappe-bench && pip install -e apps/construction_marketplace

# 4. Run migrations
bench migrate

# 5. Build assets
bench build

# 6. Clear and restart
bench --site your-site.com clear-cache
sudo supervisorctl restart all
```

---

## 14. Appendix

### 14.1 Useful Bench Commands

```bash
bench --site your-site.com console              # Python console
bench --site your-site.com migrate               # Run migrations
bench --site your-site.com clear-cache           # Clear site cache
bench --site your-site.com backup                # Create backup
bench --site your-site.com restore               # Restore from backup
bench --site your-site.com list-backups          # List available backups
bench build                                      # Build all assets
bench build --app construction_marketplace        # Build single app
bench --site your-site.com install-app {app}     # Install an app
bench --site your-site.com uninstall-app {app}   # Remove an app
bench --site your-site.com execute {path}        # Run a Python function
```

### 14.2 Key Python Functions

| Function | Purpose | How to Run |
|----------|---------|------------|
| `install.after_install()` | Post-install setup | Run by Frappe automatically |
| `install.create_all_sample_data()` | Create demo data | `bench execute construction_marketplace.install.create_all_sample_data` |
| `install.generate_material_routes()` | Generate URL routes | `bench execute construction_marketplace.install.generate_material_routes` |
| `install._fix_child_table_modules()` | Fix module paths | Called automatically during sample data creation |
| `tasks.send_low_stock_alerts()` | Daily stock check | Runs on scheduler |
| `tasks.update_order_statuses()` | Daily order check | Runs on scheduler |
| `utils.get_dashboard_data()` | Dashboard statistics | API endpoint |

### 14.3 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/method/construction_marketplace.construction_marketplace.utils.get_dashboard_data` | GET | Dashboard statistics |
| `/api/method/construction_marketplace.construction_marketplace.utils.get_material_categories` | GET | Active categories |
| `/api/method/construction_marketplace.construction_marketplace.utils.get_materials_by_category` | GET | Materials by category |
| `/api/method/construction_marketplace.construction_marketplace.utils.get_material_price` | GET | Material pricing |
| `/api/method/construction_marketplace.construction_marketplace.utils.create_order_from_enquiry` | POST | Convert enquiry to order |
| `/api/method/construction_marketplace.api.get_customer_orders` | GET | Customer order list |
| `/api/method/construction_marketplace.api.get_customer_enquiries` | GET | Customer enquiry list |
| `/api/method/construction_marketplace.api.get_dashboard_stats` | GET | Dashboard statistics |
| `/api/method/construction_marketplace.api.add_to_cart` | POST | Add item to cart |
| `/api/method/construction_marketplace.api.remove_from_cart` | POST | Remove item from cart |
| `/api/method/construction_marketplace.api.get_cart` | GET | Get cart contents |
| `/api/method/construction_marketplace.api.get_cart_count` | GET | Get cart item count |
| `/api/method/construction_marketplace.api.add_to_wishlist` | POST | Add item to wishlist |
| `/api/method/construction_marketplace.api.remove_from_wishlist` | POST | Remove item from wishlist |
| `/api/method/construction_marketplace.api.get_wishlist` | GET | Get wishlist contents |
| `/api/method/construction_marketplace.api.get_wishlist_count` | GET | Get wishlist item count |

### 14.4 Notifications

| Notification | Trigger | Recipients |
|-------------|---------|------------|
| New Order Alert | New Marketplace Order created | Construction Manager role |
| Delivery Alert | Delivery Schedule changes | Construction Manager role |
| Low Stock Alert | Stock below reorder level | Construction Manager role |

### 14.5 Custom Roles (Created on Install)

| Role | Desk Access | Home Page |
|------|-------------|-----------|
| Construction Manager | Yes | `/app/construction-marketplace` |
| Supplier | Yes | `/app/construction-marketplace` |
| Customer | Yes | `/app/construction-marketplace` |

### 14.6 File Locations

| Item | Path |
|------|------|
| App root | `~/frappe-bench/apps/construction_marketplace/` |
| Main package | `construction_marketplace/construction_marketplace/` |
| API endpoints | `construction_marketplace/construction_marketplace/api.py` |
| Website pages | `construction_marketplace/construction_marketplace/www/` |
| Static assets | `construction_marketplace/construction_marketplace/public/` |
| Workspace JSON | `construction_marketplace/construction_marketplace/workspace/construction_marketplace/construction_marketplace.json` |
| App hooks | `construction_marketplace/hooks.py` |
| Installation script | `construction_marketplace/install.py` |
| Module config | `construction_marketplace/config/desktop.py` |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | June 2026 | System | Initial SOP document |

---

*End of Document*
