"""
Scheduled Tasks for Jalali Calendar
وظایف زمان‌بندی شده
"""

import frappe
from datetime import datetime
from .api_enhanced import convert_to_jalali

def update_holiday_calendar():
    """به‌روزرسانی تقویم تعطیلات - اجرا روزانه"""
    
    # Get settings
    settings = frappe.get_single("Jalali Calendar Settings")
    if not settings.enabled or not settings.show_holidays:
        return
    
    # Get today in Jalali
    today = datetime.now()
    jalali_today = convert_to_jalali(today)
    
    if not jalali_today:
        return
    
    # Check if today is a holiday
    holidays = settings.holidays_table
    today_str = f"{jalali_today['month']:02d}/{jalali_today['day']:02d}"
    
    for holiday in holidays:
        if holiday.is_recurring:
            # Check recurring holidays (ignore year)
            holiday_date = holiday.holiday_date.split('/')[-2:]  # Get month/day
            check_date = '/'.join(holiday_date)
            
            if check_date == today_str:
                # Send notification
                send_holiday_notification(holiday.title, jalali_today)
                break

def send_holiday_notification(holiday_title, jalali_date):
    """ارسال اطلاع‌رسانی تعطیلات"""
    
    # Get all users with jalali calendar enabled
    users = frappe.get_all("User", 
                           filters={"use_jalali_calendar": 1, "enabled": 1},
                           fields=["name", "full_name"])
    
    for user in users:
        # Create notification
        notification = frappe.new_doc("Notification Log")
        notification.subject = f"تعطیل رسمی: {holiday_title}"
        notification.email_content = f"""
        <div style="direction: rtl; text-align: right;">
            <h3>تعطیل رسمی</h3>
            <p>امروز {jalali_date['formatted_long']} مصادف است با <strong>{holiday_title}</strong></p>
        </div>
        """
        notification.for_user = user.name
        notification.document_type = "Jalali Calendar Settings"
        notification.document_name = "Jalali Calendar Settings"
        
        try:
            notification.insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(f"Error sending holiday notification: {str(e)}")

def daily_calendar_sync():
    """همگام‌سازی روزانه تقویم"""
    
    # This can be extended to sync with external calendar services
    pass

def cleanup_old_notifications():
    """پاکسازی اطلاع‌رسانی‌های قدیمی"""
    
    # Delete notifications older than 30 days
    frappe.db.sql("""
        DELETE FROM `tabNotification Log`
        WHERE document_type = 'Jalali Calendar Settings'
        AND creation < DATE_SUB(NOW(), INTERVAL 30 DAY)
    """)
    
    frappe.db.commit()
