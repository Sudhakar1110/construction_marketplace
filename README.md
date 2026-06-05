# Construction Marketplace

A comprehensive Construction Materials Marketplace application built on Frappe Framework v15+ with ERPNext v15+ support.

## Overview

This app provides a complete marketplace solution for construction materials, inspired by platforms like Buildmaadi.com. It enables suppliers to list their construction materials (Cement, TMT Steel, M Sand, Bricks, Blocks, etc.) and customers to browse, enquire, and place orders seamlessly.

## Features

### Product Management
- **Material Categories**: Organize materials by type (Cement, Steel, Sand, Bricks, Blocks)
- **Material Grades**: Define grades/variants within each category (OPC 43, OPC 53, Fe 500, etc.)
- **Construction Materials**: Complete product catalog with specifications, branding, and inventory tracking

### Supplier Management
- Supplier registration and approval workflow
- Supplier rating and performance tracking
- Material pricing management per supplier

### Customer Management
- Customer registration and verification
- Customer types (Individual, Contractor, Builder, Business)

### Order Management
- Customer enquiries and quotations
- Marketplace orders with order items
- Order status workflow (Draft → Confirmed → Processing → Shipped → Delivered)
- Payment tracking and advance payment management

### Delivery Management
- Delivery scheduling and tracking
- Vehicle and driver assignment
- Delivery status tracking

### Quality Management
- Material quality inspection
- Parameter-based quality checks
- Acceptance/Rejection workflow

### Reports & Analytics
- Material Stock Report
- Sales Analysis Report
- Supplier Performance Report

### Dashboard
- Dedicated Construction Marketplace workspace
- Quick access to all key operations

## Installation

### Prerequisites
- Frappe Framework v15+
- ERPNext v15+ (optional, for enhanced functionality)

### Steps

```bash
# Go to your bench directory
cd frappe-bench

# Get the app
bench get-app https://github.com/Sudhakar1110/construction_marketplace.git

# Install on your site
bench --site your-site.com install-app construction_marketplace

# Build assets
bench build
```

## Usage

### Setting Up
1. Install the app on your site
2. Create **Material Categories** (Cement, TMT Steel, M Sand, Bricks, Blocks, Jelly Stones)
3. Create **Material Grades** (OPC 43, OPC 53, Fe 500, Fe 500D, etc.)
4. Create **Construction Materials** with specifications
5. Register **Suppliers** and set up **Material Prices**

### Order Workflow
1. Customer submits an **Enquiry** or directly places a **Marketplace Order**
2. Order is **Confirmed** and **Processed**
3. **Delivery Schedule** is created for shipment
4. **Quality Check** performed on delivered materials
5. Order marked as **Delivered** with payment completion

## Module Structure

```
construction_marketplace/
├── construction_marketplace/       # Main Python package
│   ├── hooks.py                    # App hooks and configuration
│   ├── modules.txt                 # Module registration
│   ├── config/                     # Desktop and docs configuration
│   ├── construction_marketplace/   # Module doctypes and reports
│   │   ├── doctype/                # All doctor types
│   │   ├── report/                 # Custom reports
│   │   ├── workspace/              # Dashboard workspace
│   │   └── notification/           # System notifications
│   └── public/                     # Static assets (CSS/JS)
├── requirements.txt
├── pyproject.toml
└── setup.py
```

## Doctypes

| Doctype | Description |
|---------|-------------|
| Material Category | Categories like Cement, Steel, Sand |
| Material Grade | Grades like OPC 53, Fe 500 |
| Construction Material | Product catalog with specifications |
| Supplier | Vendor/supplier information |
| Marketplace Customer | Buyer information |
| Marketplace Order | Customer orders with items |
| Customer Enquiry | Customer inquiries/quotations |
| Material Price | Pricing per material and supplier |
| Delivery Schedule | Delivery tracking |
| Quality Check | Material quality inspection |

## License

GNU General Public License v3.0

## Support

For issues and feature requests, please create an issue on GitHub.
