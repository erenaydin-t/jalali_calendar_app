"""
Print Handler for Jalali Calendar
مدیریت چاپ با تاریخ شمسی
"""

import frappe
from frappe import _
from .api_enhanced import convert_to_jalali, get_user_calendar_preference

def convert_print_dates(doc, method):
    """تبدیل تاریخ‌ها برای چاپ"""
    
    # Check if jalali calendar is enabled for printing
    if not get_user_calendar_preference():
        return
    
    settings = frappe.get_single("Jalali Calendar Settings")
    if not settings.enable_in_print:
        return
    
    # Get date fields
    meta = frappe.get_meta(doc.doctype)
    date_fields = [f.fieldname for f in meta.fields if f.fieldtype in ["Date", "Datetime"]]
    
    # Store jalali dates for printing
    doc._jalali_dates_for_print = {}
    
    for field in date_fields:
        if hasattr(doc, field) and getattr(doc, field):
            value = getattr(doc, field)
            jalali = convert_to_jalali(value)
            if jalali:
                doc._jalali_dates_for_print[field] = {
                    'short': jalali['date'],
                    'long': jalali['formatted_long'],
                    'full': f"{jalali['weekday']}، {jalali['formatted_long']}"
                }

@frappe.whitelist()
def get_print_format_with_jalali(doctype, name, print_format=None):
    """دریافت Print Format با تاریخ‌های شمسی"""
    
    doc = frappe.get_doc(doctype, name)
    
    # Convert dates
    convert_print_dates(doc, None)
    
    # Get print format
    if print_format:
        pf = frappe.get_doc("Print Format", print_format)
    else:
        pf = frappe.get_doc("Print Format", frappe.get_meta(doctype).default_print_format or "Standard")
    
    # Generate HTML with jalali dates
    html = frappe.get_print(doctype, name, print_format)
    
    # Replace dates in HTML
    if hasattr(doc, '_jalali_dates_for_print'):
        for field, dates in doc._jalali_dates_for_print.items():
            # Replace gregorian dates with jalali
            if str(getattr(doc, field)) in html:
                html = html.replace(str(getattr(doc, field)), dates['short'])
    
    return html
