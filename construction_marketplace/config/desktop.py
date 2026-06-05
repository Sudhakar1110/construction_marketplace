# Copyright (c) 2024, Sudhakar and contributors
# For license information, please see license.txt

from frappe import _

def get_data():
    return [
        {
            "module_name": "Construction Marketplace",
            "type": "module",
            "label": _("Construction Marketplace"),
            "category": "Modules",
            "_category": "Modules",
            "icon": "octicon octicon-git-branch",
            "color": "orange",
            "description": "Construction Materials Marketplace Management"
        }
    ]
