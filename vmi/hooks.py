# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "vmi"
app_title = "Erpnext Vendor Managed Inventory Vmi"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Vendor Managed Inventory Vmi - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/vmi/css/vmi.bundle.css"
app_include_js = "/assets/vmi/js/vmi.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Erpnext Vendor Managed Inventory Vmi Entry": {
        "validate": "vmi.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "vmi.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "vmi.tasks.hourly_sync"
    ],
    "daily": [
        "vmi.tasks.daily_reconciliation"
    ],
    "weekly": [
        "vmi.tasks.weekly_digest"
    ]
}
