"""
Date Converter for Document Events
مدیریت تبدیل تاریخ‌ها در هنگام ذخیره و بازیابی اسناد
"""

import frappe
from frappe import _
from .api import convert_to_gregorian, convert_to_jalali, get_user_calendar_preference
import json

def convert_dates_to_gregorian(doc, method):
    """
    تبدیل تاریخ‌های شمسی به میلادی قبل از ذخیره
    این تابع به عنوان hook در before_save استفاده می‌شود
    
    Args:
        doc: سند در حال ذخیره
        method: نام متد (before_save)
    """
    # بررسی اینکه آیا تقویم شمسی فعال است
    if not get_user_calendar_preference():
        return
    
    # بررسی وجود metadata برای تاریخ‌های تبدیل شده
    if hasattr(doc, '_jalali_dates_converted'):
        return
    
    # دریافت لیست فیلدهای تاریخ
    date_fields = get_date_fields_for_doctype(doc.doctype)
    
    for field in date_fields:
        if hasattr(doc, field) and getattr(doc, field):
            current_value = getattr(doc, field)
            
            # بررسی اینکه آیا مقدار به فرمت شمسی است
            if isinstance(current_value, str) and '/' in current_value:
                # تبدیل به میلادی
                gregorian_date = convert_to_gregorian(current_value)
                if gregorian_date:
                    setattr(doc, field, gregorian_date)
                    
                    # ذخیره مقدار اصلی شمسی برای نمایش بعدی
                    if not hasattr(doc, '_original_jalali_dates'):
                        doc._original_jalali_dates = {}
                    doc._original_jalali_dates[field] = current_value
    
    # علامت‌گذاری که تبدیل انجام شده
    doc._jalali_dates_converted = True

def after_save_conversion(doc, method):
    """
    پردازش‌های بعد از ذخیره
    
    Args:
        doc: سند ذخیره شده
        method: نام متد (on_update)
    """
    # در صورت نیاز می‌توان پردازش‌های اضافی انجام داد
    pass

def get_date_fields_for_doctype(doctype):
    """
    دریافت لیست فیلدهای تاریخ برای یک DocType
    
    Args:
        doctype: نام DocType
    
    Returns:
        list: لیست نام فیلدهای تاریخ
    """
    date_fields = []
    
    try:
        meta = frappe.get_meta(doctype)
        for field in meta.fields:
            if field.fieldtype in ['Date', 'Datetime']:
                date_fields.append(field.fieldname)
    except Exception as e:
        frappe.log_error(f"Error getting date fields for {doctype}: {str(e)}")
    
    return date_fields

@frappe.whitelist()
def get_jalali_dates_for_doc(doctype, docname):
    """
    دریافت تاریخ‌های شمسی برای یک سند
    
    Args:
        doctype: نوع سند
        docname: نام سند
    
    Returns:
        dict: دیکشنری تاریخ‌های شمسی
    """
    if not get_user_calendar_preference():
        return {}
    
    doc = frappe.get_doc(doctype, docname)
    date_fields = get_date_fields_for_doctype(doctype)
    
    jalali_dates = {}
    for field in date_fields:
        if hasattr(doc, field) and getattr(doc, field):
            value = getattr(doc, field)
            jalali_date = convert_to_jalali(value)
            if jalali_date:
                jalali_dates[field] = jalali_date
    
    return jalali_dates
