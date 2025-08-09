from . import __version__ as app_version

app_name = "jalali_calendar"
app_title = "Jalali Calendar"
app_publisher = "Your Company"
app_description = "Jalali (Shamsi) Calendar for ERPNext"
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
    "/assets/jalali_calendar/js/jalali_calendar.js"
]

# include js, css files in header of web template
# web_include_css = "/assets/jalali_calendar/css/jalali_calendar.css"
# web_include_js = "/assets/jalali_calendar/js/jalali_calendar.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "jalali_calendar/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "jalali_calendar.install.before_install"
# after_install = "jalali_calendar.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "jalali_calendar.uninstall.before_uninstall"
# after_uninstall = "jalali_calendar.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "jalali_calendar.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "*": {
        "before_save": "jalali_calendar.jalali_calendar.utils.date_converter.convert_dates_to_gregorian",
        "on_update": "jalali_calendar.jalali_calendar.utils.date_converter.after_save_conversion"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"jalali_calendar.tasks.all"
# 	],
# 	"daily": [
# 		"jalali_calendar.tasks.daily"
# 	],
# 	"hourly": [
# 		"jalali_calendar.tasks.hourly"
# 	],
# 	"weekly": [
# 		"jalali_calendar.tasks.weekly"
# 	]
# 	"monthly": [
# 		"jalali_calendar.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "jalali_calendar.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "jalali_calendar.event.get_events"
# }

# API Whitelisting
# ----------------
# Automatically whitelist methods for API access

override_whitelisted_methods = {
    "jalali_calendar.jalali_calendar.api.convert_to_jalali": "jalali_calendar.jalali_calendar.api.convert_to_jalali",
    "jalali_calendar.jalali_calendar.api.convert_to_gregorian": "jalali_calendar.jalali_calendar.api.convert_to_gregorian"
}

# API Methods
# -----------
# Methods that can be called from client side

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "jalali_calendar.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "{doctype_1}",
        "filter_by": "{filter_by}",
        "redact_fields": ["{field_1}", "{field_2}"],
        "partial": 1,
    },
    {
        "doctype": "{doctype_2}",
        "filter_by": "{filter_by}",
        "partial": 1,
    },
    {
        "doctype": "{doctype_3}",
        "strict": False,
    },
    {
        "doctype": "{doctype_4}"
    }
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"jalali_calendar.auth.validate"
# ]
