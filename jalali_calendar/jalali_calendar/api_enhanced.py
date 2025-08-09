"""
Enhanced Jalali Calendar API
توابع پیشرفته برای تبدیل و مدیریت تقویم شمسی
"""

import frappe
from frappe import _
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from datetime import datetime, date, timedelta
import json
import calendar

@frappe.whitelist()
def convert_to_jalali(gregorian_date):
    """تبدیل تاریخ میلادی به شمسی"""
    try:
        if isinstance(gregorian_date, str):
            if ' ' in gregorian_date:
                dt = datetime.strptime(gregorian_date.split('.')[0], '%Y-%m-%d %H:%M:%S')
                jalali = JalaliDateTime.to_jalali(dt)
                return {
                    'date': jalali.strftime('%Y/%m/%d'),
                    'datetime': jalali.strftime('%Y/%m/%d %H:%M:%S'),
                    'year': jalali.year,
                    'month': jalali.month,
                    'day': jalali.day,
                    'month_name': get_jalali_month_name(jalali.month),
                    'weekday': get_jalali_weekday(jalali),
                    'formatted_long': f"{jalali.day} {get_jalali_month_name(jalali.month)} {jalali.year}"
                }
            else:
                dt = datetime.strptime(gregorian_date, '%Y-%m-%d')
                jalali = JalaliDate.to_jalali(dt)
                return {
                    'date': jalali.strftime('%Y/%m/%d'),
                    'year': jalali.year,
                    'month': jalali.month,
                    'day': jalali.day,
                    'month_name': get_jalali_month_name(jalali.month),
                    'weekday': get_jalali_weekday(jalali),
                    'formatted_long': f"{jalali.day} {get_jalali_month_name(jalali.month)} {jalali.year}"
                }
        elif isinstance(gregorian_date, (date, datetime)):
            if isinstance(gregorian_date, datetime):
                jalali = JalaliDateTime.to_jalali(gregorian_date)
            else:
                jalali = JalaliDate.to_jalali(gregorian_date)
            
            return {
                'date': jalali.strftime('%Y/%m/%d'),
                'year': jalali.year,
                'month': jalali.month,
                'day': jalali.day,
                'month_name': get_jalali_month_name(jalali.month),
                'weekday': get_jalali_weekday(jalali),
                'formatted_long': f"{jalali.day} {get_jalali_month_name(jalali.month)} {jalali.year}"
            }
    except Exception as e:
        frappe.log_error(f"Error converting to Jalali: {str(e)}")
        return None

@frappe.whitelist()
def convert_to_gregorian(jalali_date_str):
    """تبدیل تاریخ شمسی به میلادی"""
    try:
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
        return jalali_date_str

def get_jalali_month_name(month_number):
    """دریافت نام ماه شمسی"""
    months = [
        'فروردین', 'اردیبهشت', 'خرداد',
        'تیر', 'مرداد', 'شهریور',
        'مهر', 'آبان', 'آذر',
        'دی', 'بهمن', 'اسفند'
    ]
    
    if 1 <= month_number <= 12:
        return months[month_number - 1]
    return ''

def get_jalali_weekday(jalali_date):
    """دریافت نام روز هفته"""
    weekdays = [
        'دوشنبه', 'سه‌شنبه', 'چهارشنبه',
        'پنج‌شنبه', 'جمعه', 'شنبه', 'یکشنبه'
    ]
    
    gregorian = jalali_date.to_gregorian()
    weekday = gregorian.weekday()
    return weekdays[weekday]

@frappe.whitelist()
def get_user_calendar_preference():
    """دریافت تنظیمات تقویم کاربر فعلی"""
    user = frappe.session.user
    
    # Check user preference first
    user_doc = frappe.get_doc("User", user)
    if hasattr(user_doc, 'use_jalali_calendar'):
        return user_doc.use_jalali_calendar
    
    # Check system settings
    if frappe.db.exists("Singles", "Jalali Calendar Settings"):
        settings = frappe.get_doc("Jalali Calendar Settings")
        return settings.enabled
    
    return False

@frappe.whitelist()
def toggle_user_calendar():
    """تغییر وضعیت تقویم برای کاربر"""
    user = frappe.session.user
    user_doc = frappe.get_doc("User", user)
    
    current_state = False
    if hasattr(user_doc, 'use_jalali_calendar'):
        current_state = user_doc.use_jalali_calendar
    
    # Toggle the state
    new_state = not current_state
    frappe.db.set_value("User", user, "use_jalali_calendar", new_state)
    frappe.db.commit()
    
    return new_state

@frappe.whitelist()
def bulk_convert_dates(dates_dict):
    """تبدیل دسته‌ای تاریخ‌ها"""
    if isinstance(dates_dict, str):
        dates_dict = json.loads(dates_dict)
    
    converted = {}
    for field_name, date_value in dates_dict.items():
        if date_value:
            converted[field_name] = convert_to_jalali(date_value)
    
    return converted

@frappe.whitelist()
def get_month_calendar(year=None, month=None):
    """دریافت تقویم ماه به صورت HTML"""
    try:
        # Get current Jalali date if not provided
        if not year or not month:
            today = datetime.now()
            jalali_today = JalaliDate.to_jalali(today)
            year = jalali_today.year if not year else year
            month = jalali_today.month if not month else month
        
        # Get first and last day of month
        first_day = JalaliDate(year, month, 1)
        
        # Get number of days in month
        if month <= 6:
            days_in_month = 31
        elif month <= 11:
            days_in_month = 30
        else:
            # Check for leap year
            days_in_month = 30 if first_day.is_leap() else 29
        
        # Create calendar HTML
        html = f"""
        <div class="jalali-calendar-widget">
            <h4>{get_jalali_month_name(month)} {year}</h4>
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>ش</th><th>ی</th><th>د</th><th>س</th><th>چ</th><th>پ</th><th>ج</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        # Get weekday of first day
        first_gregorian = first_day.to_gregorian()
        first_weekday = (first_gregorian.weekday() + 2) % 7  # Adjust for Saturday start
        
        # Fill calendar
        html += "<tr>"
        
        # Empty cells before first day
        for i in range(first_weekday):
            html += "<td></td>"
        
        # Days of month
        current_day = 1
        current_weekday = first_weekday
        
        while current_day <= days_in_month:
            if current_weekday == 7:
                html += "</tr><tr>"
                current_weekday = 0
            
            # Check if today
            today_jalali = JalaliDate.to_jalali(datetime.now())
            is_today = (today_jalali.year == year and 
                       today_jalali.month == month and 
                       today_jalali.day == current_day)
            
            class_name = "text-primary font-weight-bold" if is_today else ""
            html += f'<td class="{class_name}">{current_day}</td>'
            
            current_day += 1
            current_weekday += 1
        
        # Empty cells after last day
        while current_weekday < 7:
            html += "<td></td>"
            current_weekday += 1
        
        html += """
                </tr>
                </tbody>
            </table>
        </div>
        """
        
        return html
        
    except Exception as e:
        frappe.log_error(f"Error generating calendar: {str(e)}")
        return "<p>خطا در نمایش تقویم</p>"

@frappe.whitelist()
def get_holidays(year=None):
    """دریافت تعطیلات رسمی سال"""
    if not year:
        today = datetime.now()
        jalali_today = JalaliDate.to_jalali(today)
        year = jalali_today.year
    
    # لیست تعطیلات ثابت (نمونه)
    holidays = [
        {"date": f"{year}/01/01", "title": "عید نوروز"},
        {"date": f"{year}/01/02", "title": "عید نوروز"},
        {"date": f"{year}/01/03", "title": "عید نوروز"},
        {"date": f"{year}/01/04", "title": "عید نوروز"},
        {"date": f"{year}/01/12", "title": "روز جمهوری اسلامی"},
        {"date": f"{year}/01/13", "title": "سیزده بدر"},
        {"date": f"{year}/03/14", "title": "رحلت امام خمینی"},
        {"date": f"{year}/03/15", "title": "قیام 15 خرداد"},
        {"date": f"{year}/11/22", "title": "پیروزی انقلاب اسلامی"},
        {"date": f"{year}/12/29", "title": "روز ملی شدن صنعت نفت"},
    ]
    
    return holidays

@frappe.whitelist()
def format_for_print(date_value, format_type="short"):
    """فرمت تاریخ برای چاپ"""
    jalali = convert_to_jalali(date_value)
    if not jalali:
        return date_value
    
    if format_type == "long":
        return jalali['formatted_long']
    elif format_type == "full":
        return f"{jalali['weekday']}، {jalali['formatted_long']}"
    else:
        return jalali['date']

@frappe.whitelist()
def get_date_range(from_date, to_date, format="short"):
    """دریافت بازه تاریخی به شمسی"""
    from_jalali = convert_to_jalali(from_date)
    to_jalali = convert_to_jalali(to_date)
    
    if not from_jalali or not to_jalali:
        return None
    
    if format == "long":
        return f"از {from_jalali['formatted_long']} تا {to_jalali['formatted_long']}"
    else:
        return f"از {from_jalali['date']} تا {to_jalali['date']}"

@frappe.whitelist()
def validate_jalali_date(jalali_date_str):
    """اعتبارسنجی تاریخ شمسی"""
    try:
        parts = jalali_date_str.replace('/', '-').split('-')
        if len(parts) != 3:
            return {"valid": False, "error": "فرمت تاریخ نادرست است"}
        
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        
        # Check ranges
        if not (1300 <= year <= 1500):
            return {"valid": False, "error": "سال باید بین 1300 تا 1500 باشد"}
        
        if not (1 <= month <= 12):
            return {"valid": False, "error": "ماه باید بین 1 تا 12 باشد"}
        
        # Check day based on month
        if month <= 6:
            max_day = 31
        elif month <= 11:
            max_day = 30
        else:
            # Check for leap year
            jalali = JalaliDate(year, 1, 1)
            max_day = 30 if jalali.is_leap() else 29
        
        if not (1 <= day <= max_day):
            return {"valid": False, "error": f"روز باید بین 1 تا {max_day} باشد"}
        
        # Try to create the date
        jalali = JalaliDate(year, month, day)
        gregorian = jalali.to_gregorian()
        
        return {
            "valid": True,
            "gregorian": gregorian.strftime('%Y-%m-%d'),
            "formatted": f"{day} {get_jalali_month_name(month)} {year}"
        }
        
    except Exception as e:
        return {"valid": False, "error": str(e)}

@frappe.whitelist()
def export_with_jalali(doctype, filters=None):
    """Export data with Jalali dates"""
    # Get data
    data = frappe.get_list(doctype, filters=filters, fields=["*"])
    
    # Get date fields
    meta = frappe.get_meta(doctype)
    date_fields = [f.fieldname for f in meta.fields if f.fieldtype in ["Date", "Datetime"]]
    
    # Convert dates
    for row in data:
        for field in date_fields:
            if field in row and row[field]:
                jalali = convert_to_jalali(row[field])
                if jalali:
                    row[f"{field}_jalali"] = jalali['date']
    
    return data
