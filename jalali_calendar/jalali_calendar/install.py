"""
After Install Script for Jalali Calendar
ایجاد خودکار فیلدها و تنظیمات اولیه
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def after_install():
    """اجرا بعد از نصب App"""
    print("Setting up Jalali Calendar...")
    
    # Create custom fields
    create_user_custom_field()
    create_system_settings_field()
    
    # Create default settings
    create_default_settings()
    
    # Add default holidays
    add_default_holidays()
    
    # Clear cache
    frappe.clear_cache()
    
    print("Jalali Calendar setup completed!")

def create_user_custom_field():
    """ایجاد فیلد سفارشی برای User"""
    if not frappe.db.exists("Custom Field", "User-use_jalali_calendar"):
        create_custom_field("User", {
            "fieldname": "use_jalali_calendar",
            "label": "استفاده از تقویم شمسی",
            "fieldtype": "Check",
            "insert_after": "language",
            "description": "فعال‌سازی تقویم شمسی برای این کاربر"
        })
        print("✓ User custom field created")

def create_system_settings_field():
    """ایجاد فیلد سفارشی برای System Settings"""
    if not frappe.db.exists("Custom Field", "System Settings-use_jalali_calendar"):
        create_custom_field("System Settings", {
            "fieldname": "use_jalali_calendar",
            "label": "تقویم شمسی پیش‌فرض",
            "fieldtype": "Check",
            "insert_after": "language",
            "description": "فعال‌سازی تقویم شمسی به صورت پیش‌فرض برای کاربران جدید"
        })
        print("✓ System Settings custom field created")

def create_default_settings():
    """ایجاد تنظیمات پیش‌فرض"""
    if not frappe.db.exists("Jalali Calendar Settings"):
        settings = frappe.new_doc("Jalali Calendar Settings")
        settings.enabled = 1
        settings.system_wide = 0
        settings.date_format = "YYYY/MM/DD"
        settings.datetime_format = "YYYY/MM/DD HH:mm"
        settings.first_day_of_week = "6"
        settings.show_holidays = 1
        settings.enable_in_lists = 1
        settings.enable_in_reports = 1
        settings.enable_in_print = 1
        settings.enable_keyboard_shortcuts = 1
        settings.auto_convert_imports = 0
        
        try:
            settings.insert(ignore_permissions=True)
            print("✓ Default settings created")
        except Exception as e:
            print(f"Error creating settings: {e}")

def add_default_holidays():
    """اضافه کردن تعطیلات پیش‌فرض"""
    holidays = [
        {"date": "01/01", "title": "عید نوروز", "recurring": True},
        {"date": "01/02", "title": "عید نوروز", "recurring": True},
        {"date": "01/03", "title": "عید نوروز", "recurring": True},
        {"date": "01/04", "title": "عید نوروز", "recurring": True},
        {"date": "01/12", "title": "روز جمهوری اسلامی", "recurring": True},
        {"date": "01/13", "title": "سیزده بدر", "recurring": True},
        {"date": "03/14", "title": "رحلت امام خمینی", "recurring": True},
        {"date": "03/15", "title": "قیام 15 خرداد", "recurring": True},
        {"date": "11/22", "title": "پیروزی انقلاب اسلامی", "recurring": True},
        {"date": "12/29", "title": "روز ملی شدن صنعت نفت", "recurring": True},
    ]
    
    try:
        settings = frappe.get_doc("Jalali Calendar Settings")
        
        for holiday in holidays:
            settings.append("holidays_table", {
                "holiday_date": holiday["date"],
                "title": holiday["title"],
                "is_recurring": holiday["recurring"]
            })
        
        settings.save(ignore_permissions=True)
        print(f"✓ {len(holidays)} default holidays added")
    except Exception as e:
        print(f"Error adding holidays: {e}")

def before_uninstall():
    """اجرا قبل از حذف App"""
    # Remove custom fields
    frappe.delete_doc("Custom Field", "User-use_jalali_calendar", ignore_permissions=True, force=True)
    frappe.delete_doc("Custom Field", "System Settings-use_jalali_calendar", ignore_permissions=True, force=True)
    
    print("Jalali Calendar custom fields removed")
