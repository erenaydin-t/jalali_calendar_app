"""
Jinja Filters for Jalali Calendar
فیلترهای Jinja برای استفاده در قالب‌ها
"""

from .api_enhanced import convert_to_jalali, format_for_print

def to_jalali(date_value, format="short"):
    """فیلتر Jinja برای تبدیل به شمسی
    
    Usage in template:
    {{ doc.posting_date | to_jalali }}
    {{ doc.posting_date | to_jalali("long") }}
    """
    if not date_value:
        return ""
    
    return format_for_print(date_value, format)

def jalali_format(date_value, pattern="YYYY/MM/DD"):
    """فیلتر Jinja برای فرمت دلخواه تاریخ شمسی
    
    Usage in template:
    {{ doc.posting_date | jalali_format("DD MMMM YYYY") }}
    """
    if not date_value:
        return ""
    
    jalali = convert_to_jalali(date_value)
    if not jalali:
        return date_value
    
    # Replace patterns
    result = pattern
    result = result.replace("YYYY", str(jalali['year']))
    result = result.replace("YY", str(jalali['year'])[2:])
    result = result.replace("MMMM", jalali['month_name'])
    result = result.replace("MM", str(jalali['month']).zfill(2))
    result = result.replace("M", str(jalali['month']))
    result = result.replace("DD", str(jalali['day']).zfill(2))
    result = result.replace("D", str(jalali['day']))
    
    return result

def jalali_now(format="short"):
    """دریافت تاریخ امروز به شمسی
    
    Usage in template:
    {{ jalali_now() }}
    {{ jalali_now("long") }}
    """
    from datetime import datetime
    return format_for_print(datetime.now(), format)

def jalali_month_name(month_number):
    """دریافت نام ماه شمسی
    
    Usage in template:
    {{ 5 | jalali_month_name }}  => مرداد
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
