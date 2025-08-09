from . import __version__ as app_version

app_name = "jalali_calendar"
app_title = "Jalali Calendar"
app_publisher = "Your Company"
app_description = "Complete Jalali (Shamsi) Calendar Integration for ERPNext"
app_icon = "octicon octicon-calendar"
app_color = "green"
app_email = "your.email@example.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = [
    "/assets/jalali_calendar/css/jalali_calendar.css",
    "/assets/jalali_calendar/css/persianDatepicker.css"
]

app_include_js = [
    "/assets/jalali_calendar/js/moment-jalaali.min.js",
    "/assets/jalali_calendar/js/persianDatepicker.min.js", 
    "/assets/jalali_calendar/js/jalali_calendar_enhanced.js"
]

# include js, css files in header of web template
web_include_css = "/assets/jalali_calendar/css/jalali_calendar.css"
web_include_js = "/assets/jalali_calendar/js/jalali_calendar_enhanced.js"

# Installation
# ------------

before_install = "jalali_calendar.jalali_calendar.install.before_install"
after_install = "jalali_calendar.jalali_calendar.install.after_install"

# Uninstallation
# ------------

before_uninstall = "jalali_calendar.jalali_calendar.install.before_uninstall"

# Document Events
# ---------------

doc_events = {
    "*": {
        "before_save": "jalali_calendar.jalali_calendar.utils.date_converter.convert_dates_to_gregorian",
        "on_update": "jalali_calendar.jalali_calendar.utils.date_converter.after_save_conversion",
        "before_print": "jalali_calendar.jalali_calendar.utils.print_handler.convert_print_dates"
    }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "daily": [
        "jalali_calendar.jalali_calendar.tasks.update_holiday_calendar"
    ]
}

# Override Methods
# ----------------

override_whitelisted_methods = {
    # Report handling
    "frappe.desk.query_report.run": "jalali_calendar.jalali_calendar.report_handler.run_report_with_jalali",
    "frappe.desk.query_report.export_query": "jalali_calendar.jalali_calendar.report_handler.export_report_with_jalali",
    
    # API methods
    "jalali_calendar.jalali_calendar.api_enhanced.convert_to_jalali": "jalali_calendar.jalali_calendar.api_enhanced.convert_to_jalali",
    "jalali_calendar.jalali_calendar.api_enhanced.convert_to_gregorian": "jalali_calendar.jalali_calendar.api_enhanced.convert_to_gregorian",
    "jalali_calendar.jalali_calendar.api_enhanced.get_user_calendar_preference": "jalali_calendar.jalali_calendar.api_enhanced.get_user_calendar_preference",
    "jalali_calendar.jalali_calendar.api_enhanced.toggle_user_calendar": "jalali_calendar.jalali_calendar.api_enhanced.toggle_user_calendar",
    "jalali_calendar.jalali_calendar.api_enhanced.get_month_calendar": "jalali_calendar.jalali_calendar.api_enhanced.get_month_calendar",
    "jalali_calendar.jalali_calendar.api_enhanced.get_holidays": "jalali_calendar.jalali_calendar.api_enhanced.get_holidays",
    "jalali_calendar.jalali_calendar.api_enhanced.validate_jalali_date": "jalali_calendar.jalali_calendar.api_enhanced.validate_jalali_date",
    "jalali_calendar.jalali_calendar.api_enhanced.export_with_jalali": "jalali_calendar.jalali_calendar.api_enhanced.export_with_jalali",
    "jalali_calendar.jalali_calendar.api_enhanced.format_for_print": "jalali_calendar.jalali_calendar.api_enhanced.format_for_print",
    "jalali_calendar.jalali_calendar.api_enhanced.get_date_range": "jalali_calendar.jalali_calendar.api_enhanced.get_date_range"
}

# Jinja Filters
# -------------

jinja = {
    "methods": [
        "jalali_calendar.jalali_calendar.api_enhanced.convert_to_jalali",
        "jalali_calendar.jalali_calendar.api_enhanced.format_for_print"
    ],
    "filters": [
        "jalali_calendar.jalali_calendar.utils.jinja_filters.to_jalali",
        "jalali_calendar.jalali_calendar.utils.jinja_filters.jalali_format"
    ]
}

# Fixtures
# --------

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            ["name", "in", ["User-use_jalali_calendar", "System Settings-use_jalali_calendar"]]
        ]
    },
    {
        "doctype": "Jalali Calendar Settings"
    }
]

# Website
# -------

website_route_rules = [
    {
        "from_route": "/jalali-calendar",
        "to_route": "jalali_calendar"
    }
]

# Permissions
# -----------

has_permission = {
    "Jalali Calendar Settings": "jalali_calendar.jalali_calendar.permissions.has_permission"
}

# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "User",
        "filter_by": "name",
        "redact_fields": [],
        "partial": 1,
    }
]
