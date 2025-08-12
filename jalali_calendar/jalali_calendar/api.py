import frappe
from frappe import _
import jdatetime
from datetime import datetime
from persiantools.jdatetime import JalaliDate, JalaliDateTime

@frappe.whitelist()
def get_user_calendar_preference():
    """Get user's calendar preference"""
    try:
        # Check user preference
        user_preference = frappe.db.get_value("User", frappe.session.user, "use_jalali_calendar")
        if user_preference:
            return True
        
        # Check system setting
        system_preference = frappe.db.get_single_value("System Settings", "use_jalali_calendar")
        return system_preference or False
    except:
        return False

@frappe.whitelist()
def convert_to_jalali(date_str):
    """Convert Gregorian date to Jalali"""
    try:
        if not date_str:
            return ""
        
        # Parse the date string
        if isinstance(date_str, str):
            # Try different date formats
            for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d']:
                try:
                    date_obj = datetime.strptime(date_str, fmt).date()
                    break
                except ValueError:
                    continue
            else:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date_obj = date_str
        
        # Convert to Jalali using jdatetime
        jalali_date = jdatetime.date.fromgregorian(date=date_obj)
        
        # Get month name
        month_names = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
                      'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
        
        # Return formatted Jalali date
        return {
            'formatted': jalali_date.strftime('%Y/%m/%d'),
            'year': jalali_date.year,
            'month': jalali_date.month,
            'day': jalali_date.day,
            'month_name': month_names[jalali_date.month - 1]
        }
    except Exception as e:
        frappe.log_error(f"Error converting to Jalali: {str(e)}")
        return {'formatted': date_str, 'error': str(e)}

@frappe.whitelist()
def convert_to_gregorian(date_str):
    """Convert Jalali date to Gregorian"""
    try:
        if not date_str:
            return ""
        
        # Parse Jalali date (expected format: YYYY/MM/DD or YYYY-MM-DD)
        date_str = date_str.replace('-', '/')
        parts = date_str.split('/')
        if len(parts) != 3:
            return date_str
        
        year, month, day = map(int, parts)
        
        # Create Jalali date object
        jalali_date = jdatetime.date(year, month, day)
        
        # Convert to Gregorian
        gregorian_date = jalali_date.togregorian()
        
        # Return formatted date
        return gregorian_date.strftime('%Y-%m-%d')
    except Exception as e:
        frappe.log_error(f"Error converting to Gregorian: {str(e)}")
        return date_str

@frappe.whitelist()
def get_jalali_date_for_field(doctype, docname, fieldname):
    """Get Jalali date for a specific field"""
    try:
        if not frappe.has_permission(doctype, 'read'):
            frappe.throw(_('Insufficient Permission'))
            
        doc = frappe.get_doc(doctype, docname)
        date_value = doc.get(fieldname)
        
        if date_value:
            return convert_to_jalali(str(date_value))
        
        return {'formatted': '', 'error': 'No date value'}
    except Exception as e:
        frappe.log_error(f"Error getting Jalali date: {str(e)}")
        return {'formatted': '', 'error': str(e)}