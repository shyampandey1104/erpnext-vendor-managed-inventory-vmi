# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "vmi"
app_title = "Erpnext Vendor Managed Inventory Vmi"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Vendor Managed Inventory Vmi for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/vmi/css/vmi.bundle.css"
app_include_js = "/assets/vmi/js/vmi.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "vmi.engine.on_document_submit",
        "on_cancel": "vmi.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "vmi.engine.daily_scheduled_sync"
    ]
}
