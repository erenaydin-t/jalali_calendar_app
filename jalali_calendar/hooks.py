app_name = "jalali_calendar"
app_title = "Jalali Calendar"
app_publisher = "Eren Aydin"
app_description = "Jalali (Shamsi) Calendar for ERPNext"
app_email = "*****@gmail.com"
app_license = "MIT"
app_version = "1.0.0"
app_icon = "octicon octicon-calendar"
app_color = "green"

# Include JS/CSS files in the app
app_include_js = [
    "/assets/jalali_calendar/js/moment-jalaali.min.js",
    "/assets/jalali_calendar/js/persianDatepicker.min.js",
    "/assets/jalali_calendar/js/jalali_calendar.js"
]

app_include_css = [
    "/assets/jalali_calendar/css/jalali_calendar.css",
    "/assets/jalali_calendar/css/persianDatepicker.css"
]

# Document Events
doc_events = {
    "*": {
        "before_save": ["jalali_calendar.jalali_calendar.utils.date_converter.convert_dates_to_gregorian"],
        "on_update": ["jalali_calendar.jalali_calendar.utils.date_converter.after_save_conversion"]
    }
}

# Whitelisted Methods for API
override_whitelisted_methods = {
    "jalali_calendar.jalali_calendar.api.convert_to_jalali": "jalali_calendar.jalali_calendar.api.convert_to_jalali",
    "jalali_calendar.jalali_calendar.api.convert_to_gregorian": "jalali_calendar.jalali_calendar.api.convert_to_gregorian",
    "jalali_calendar.jalali_calendar.api.get_user_calendar_preference": "jalali_calendar.jalali_calendar.api.get_user_calendar_preference",
    "jalali_calendar.jalali_calendar.api.get_jalali_date_for_field": "jalali_calendar.jalali_calendar.api.get_jalali_date_for_field"
}

# Fixtures - Custom fields for User and System Settings
fixtures = ["Custom Field"]