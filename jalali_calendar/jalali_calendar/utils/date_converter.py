import frappe
from datetime import datetime
import jdatetime
from persiantools.jdatetime import JalaliDate, JalaliDateTime

def gregorian_to_jalali(gregorian_date):
    """Convert a Gregorian date to Jalali date"""
    try:
        if not gregorian_date:
            return None
            
        if isinstance(gregorian_date, str):
            # Try different date formats
            for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d']:
                try:
                    gregorian_date = datetime.strptime(gregorian_date, fmt).date()
                    break
                except ValueError:
                    continue
            else:
                gregorian_date = datetime.strptime(gregorian_date, '%Y-%m-%d').date()
                
        jalali = jdatetime.date.fromgregorian(date=gregorian_date)
        return jalali.strftime('%Y/%m/%d')
    except Exception as e:
        frappe.log_error(f"Error in gregorian_to_jalali: {str(e)}")
        return None

def jalali_to_gregorian(jalali_date):
    """Convert a Jalali date to Gregorian date"""
    try:
        if not jalali_date:
            return None
            
        # Parse Jalali date string
        if isinstance(jalali_date, str):
            jalali_date = jalali_date.replace('-', '/')
            parts = jalali_date.split('/')
            if len(parts) != 3:
                return None
            year, month, day = map(int, parts)
            jalali = jdatetime.date(year, month, day)
        else:
            jalali = jalali_date
            
        gregorian = jalali.togregorian()
        return gregorian.strftime('%Y-%m-%d')
    except Exception as e:
        frappe.log_error(f"Error in jalali_to_gregorian: {str(e)}")
        return None

def get_user_calendar_preference():
    """Check if user prefers Jalali calendar"""
    try:
        # Check user preference first
        user_preference = frappe.db.get_value("User", frappe.session.user, "use_jalali_calendar")
        if user_preference:
            return True
        
        # Check system-wide setting
        system_preference = frappe.db.get_single_value("System Settings", "use_jalali_calendar")
        return system_preference or False
    except:
        return False

def format_date_for_user(date_value):
    """Format date based on user's calendar preference"""
    try:
        if not date_value:
            return ""
            
        # Check if user prefers Jalali calendar
        if get_user_calendar_preference():
            return gregorian_to_jalali(date_value) or str(date_value)
                
        return str(date_value)
    except Exception as e:
        frappe.log_error(f"Error in format_date_for_user: {str(e)}")
        return str(date_value)

def convert_dates_to_gregorian(doc, method=None):
    """Convert Jalali dates to Gregorian before saving"""
    try:
        # Get all date and datetime fields
        meta = frappe.get_meta(doc.doctype)
        date_fields = [df.fieldname for df in meta.fields if df.fieldtype in ['Date', 'Datetime']]
        
        for field in date_fields:
            value = doc.get(field)
            if value and isinstance(value, str) and '/' in value:
                # This might be a Jalali date
                gregorian = jalali_to_gregorian(value)
                if gregorian:
                    doc.set(field, gregorian)
    except Exception as e:
        frappe.log_error(f"Error converting dates to Gregorian: {str(e)}")

def after_save_conversion(doc, method=None):
    """Post-save processing for date conversion"""
    try:
        # This function can be used for any post-save date processing
        # Currently empty but kept for future extensions
        pass
    except Exception as e:
        frappe.log_error(f"Error in after_save_conversion: {str(e)}")

def get_jalali_months():
    """Get list of Jalali month names"""
    return [
        'فروردین', 'اردیبهشت', 'خرداد', 
        'تیر', 'مرداد', 'شهریور',
        'مهر', 'آبان', 'آذر', 
        'دی', 'بهمن', 'اسفند'
    ]

def get_current_jalali_date():
    """Get current date in Jalali calendar"""
    try:
        today = datetime.now()
        jalali = jdatetime.datetime.now()
        
        return {
            'date': jalali.strftime('%Y/%m/%d'),
            'time': jalali.strftime('%H:%M:%S'),
            'year': jalali.year,
            'month': jalali.month,
            'day': jalali.day,
            'month_name': get_jalali_months()[jalali.month - 1]
        }
    except Exception as e:
        frappe.log_error(f"Error getting current Jalali date: {str(e)}")
        return None