"""
Permissions Handler for Jalali Calendar
مدیریت دسترسی‌ها
"""

import frappe
from frappe import _

def has_permission(doc, ptype, user):
    """بررسی دسترسی به تنظیمات تقویم شمسی"""
    
    # System Manager has full access
    if "System Manager" in frappe.get_roles(user):
        return True
    
    # HR Manager can view and update
    if "HR Manager" in frappe.get_roles(user):
        if ptype in ["read", "write"]:
            return True
    
    # All users can read their own preferences
    if ptype == "read":
        return True
    
    return False

def get_permission_query_conditions(user):
    """شرایط query برای دسترسی‌ها"""
    
    if "System Manager" in frappe.get_roles(user):
        return None
    
    return f"(`tabJalali Calendar Settings`.`owner` = {frappe.db.escape(user)})"

def can_set_user_permissions(doc, ptype, user):
    """آیا کاربر می‌تواند دسترسی‌های دیگران را تنظیم کند"""
    
    return "System Manager" in frappe.get_roles(user)
