"""
Jalali Calendar Converter Module
تبدیل تاریخ‌های شمسی به میلادی و بالعکس
"""

import frappe
from frappe import _
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from datetime import datetime, date
import json

@frappe.whitelist()
def convert_to_jalali(gregorian_date):
    """
    تبدیل تاریخ میلادی به شمسی
    
    Args:
        gregorian_date: تاریخ میلادی به فرمت string یا date object
    
    Returns:
        dict: حاوی تاریخ شمسی به فرمت‌های مختلف
    """
    try:
        if isinstance(gregorian_date, str):
            # تبدیل string به date object
            if ' ' in gregorian_date:
                dt = datetime.strptime(gregorian_date, '%Y-%m-%d %H:%M:%S')
                jalali = JalaliDateTime.to_jalali(dt)
                return {
                    'date': jalali.strftime('%Y/%m/%d'),
                    'datetime': jalali.strftime('%Y/%m/%d %H:%M:%S'),
                    'year': jalali.year,
                    'month': jalali.month,
                    'day': jalali.day,
                    'month_name': get_jalali_month_name(jalali.month)
                }
            else:
                dt = datetime.strptime(gregorian_date, '%Y-%m-%d')
                jalali = JalaliDate.to_jalali(dt)
                return {
                    'date': jalali.strftime('%Y/%m/%d'),
                    'year': jalali.year,
                    'month': jalali.month,
                    'day': jalali.day,
                    'month_name': get_jalali_month_name(jalali.month)
                }
        elif isinstance(gregorian_date, (date, datetime)):
            if isinstance(gregorian_date, datetime):
                jalali = JalaliDateTime.to_jalali(gregorian_date)
                return {
                    'date': jalali.strftime('%Y/%m/%d'),
                    'datetime': jalali.strftime('%Y/%m/%d %H:%M:%S'),
                    'year': jalali.year,
                    'month': jalali.month,
                    'day': jalali.day,
                    'month_name': get_jalali_month_name(jalali.month)
                }
            else:
                jalali = JalaliDate.to_jalali(gregorian_date)
                return {
                    'date': jalali.strftime('%Y/%m/%d'),
                    'year': jalali.year,
                    'month': jalali.month,
                    'day': jalali.day,
                    'month_name': get_jalali_month_name(jalali.month)
                }
    except Exception as e:
        frappe.log_error(f"Error converting to Jalali: {str(e)}")
        return None

@frappe.whitelist()
def convert_to_gregorian(jalali_date_str):
    """
    تبدیل تاریخ شمسی به میلادی
    
    Args:
        jalali_date_str: تاریخ شمسی به فرمت string (مثلا: 1402/10/15)
    
    Returns:
        str: تاریخ میلادی به فرمت Y-m-d
    """
    try:
        # حذف اسلش‌ها و تبدیل به فرمت مناسب
        parts = jalali_date_str.replace('/', '-').split('-')
        if len(parts) == 3:
            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])
            
            jalali = JalaliDate(year, month, day)
            gregorian = jalali.to_gregorian()
            
            return gregorian.strftime('%Y-%m-%d')
    except Exception as e:
        frappe.log_error(f"Error converting to Gregorian: {str(e)}")
        return jalali_date_str  # در صورت خطا، همان مقدار اولیه را برگردان

def get_jalali_month_name(month_number):
    """
    دریافت نام ماه شمسی
    
    Args:
        month_number: شماره ماه (1-12)
    
    Returns:
        str: نام ماه به فارسی
    """
    months = [
        'فروردین', 'اردیبهشت', 'خرداد',
        'تیر', 'مرداد', 'شهریور',
        'مهر', 'آبان', 'آذر',
        'دی', 'بهمن', 'اسفند'
    ]
    
    if 1 <= month_number <= 12:
        return months[month_number - 1]
    return ''

@frappe.whitelist()
def get_user_calendar_preference():
    """
    دریافت تنظیمات تقویم کاربر فعلی
    
    Returns:
        bool: آیا تقویم شمسی فعال است یا خیر
    """
    user = frappe.session.user
    user_doc = frappe.get_doc("User", user)
    
    # بررسی فیلد سفارشی برای تنظیمات تقویم
    if hasattr(user_doc, 'use_jalali_calendar'):
        return user_doc.use_jalali_calendar
    
    # بررسی تنظیمات سیستم
    return frappe.db.get_single_value('System Settings', 'use_jalali_calendar') or False

@frappe.whitelist()
def bulk_convert_dates(dates_dict):
    """
    تبدیل دسته‌ای تاریخ‌ها
    
    Args:
        dates_dict: دیکشنری حاوی تاریخ‌ها
    
    Returns:
        dict: دیکشنری تاریخ‌های تبدیل شده
    """
    if isinstance(dates_dict, str):
        dates_dict = json.loads(dates_dict)
    
    converted = {}
    for field_name, date_value in dates_dict.items():
        if date_value:
            converted[field_name] = convert_to_jalali(date_value)
    
    return converted
