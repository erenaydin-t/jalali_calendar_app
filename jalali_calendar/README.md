# Jalali Calendar App for ERPNext 15

یک Custom App برای اضافه کردن قابلیت تقویم شمسی (جلالی) به ERPNext

## ویژگی‌ها
- نمایش تاریخ‌ها به صورت شمسی در تمام فرم‌ها
- ذخیره‌سازی به صورت میلادی در دیتابیس
- قابلیت فعال/غیرفعال کردن برای هر کاربر
- سازگار با ERPNext 15

## نصب

```bash
# در پوشه frappe-bench
bench get-app jalali_calendar https://github.com/yourusername/jalali_calendar
bench --site your-site-name install-app jalali_calendar
```

## استفاده
بعد از نصب، به بخش تنظیمات بروید و Jalali Calendar را فعال کنید.

## Requirements
- ERPNext 15
- Frappe Framework 15
