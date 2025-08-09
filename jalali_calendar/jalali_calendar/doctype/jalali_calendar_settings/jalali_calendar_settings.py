# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class JalaliCalendarSettings(Document):
    def validate(self):
        """Validate settings"""
        # Ensure date format is valid
        if not self.date_format:
            self.date_format = "YYYY/MM/DD"
        
        if not self.datetime_format:
            self.datetime_format = "YYYY/MM/DD HH:mm"
    
    def on_update(self):
        """Clear cache after updating settings"""
        frappe.clear_cache()
        
        # If system-wide is enabled, update all users
        if self.system_wide:
            frappe.db.sql("""
                UPDATE `tabUser`
                SET use_jalali_calendar = 1
                WHERE name != 'Administrator'
            """)
            frappe.db.commit()
            
            frappe.msgprint("تقویم شمسی برای همه کاربران فعال شد", indicator="green")
    
    @frappe.whitelist()
    def reset_to_defaults(self):
        """Reset settings to default values"""
        self.date_format = "YYYY/MM/DD"
        self.datetime_format = "YYYY/MM/DD HH:mm"
        self.first_day_of_week = "6"
        self.show_holidays = 1
        self.enable_in_lists = 1
        self.enable_in_reports = 1
        self.enable_in_print = 1
        self.enable_keyboard_shortcuts = 1
        self.save()
        
        return "تنظیمات به حالت پیش‌فرض بازگشت"
