# راهنمای نصب Jalali Calendar App برای ERPNext 15

## پیش‌نیازها
1. ERPNext 15 نصب شده
2. دسترسی به Bench
3. Python 3.8+

## مراحل نصب

### 1. کپی کردن App به پوشه Bench

پوشه `jalali_calendar` را به مسیر `frappe-bench/apps/` کپی کنید.

### 2. نصب Dependencies

#### Python Dependencies:
```bash
pip install persiantools jdatetime
```

### 3. نصب App در Site

```bash
cd frappe-bench
bench --site [your-site-name] install-app jalali_calendar
```

### 4. دانلود JavaScript Libraries

#### Moment-Jalaali:
دانلود از: https://unpkg.com/moment-jalaali@latest/build/moment-jalaali.js
ذخیره در: `apps/jalali_calendar/public/js/moment-jalaali.min.js`

#### Persian Datepicker:
دانلود از: https://github.com/behzadi/persianDatepicker
فایل‌های مورد نیاز:
- `persianDatepicker.min.js` → `apps/jalali_calendar/public/js/`
- `persianDatepicker.css` → `apps/jalali_calendar/public/css/`

### 5. Build Assets

```bash
bench build --app jalali_calendar
```

### 6. اضافه کردن Custom Fields

در ERPNext به Customize Form بروید و:

#### برای User DocType:
- Field Label: Use Jalali Calendar
- Field Type: Check
- Field Name: use_jalali_calendar

#### برای System Settings:
- Field Label: Use Jalali Calendar (System Wide)
- Field Type: Check
- Field Name: use_jalali_calendar

### 7. Clear Cache و Restart

```bash
bench --site [your-site-name] clear-cache
bench restart
```

## تنظیمات

### فعال‌سازی برای کاربر:
1. به User Settings بروید
2. گزینه "Use Jalali Calendar" را فعال کنید
3. ذخیره کنید

### فعال‌سازی سیستمی:
1. به System Settings بروید
2. گزینه "Use Jalali Calendar" را فعال کنید
3. ذخیره کنید

## تست

1. یک فرم جدید باز کنید (مثلاً Sales Invoice)
2. در فیلدهای تاریخ، باید تاریخ شمسی نمایش داده شود
3. با انتخاب تاریخ، datepicker شمسی باز شود
4. بعد از ذخیره، تاریخ به صورت میلادی در دیتابیس ذخیره می‌شود

## عیب‌یابی

### اگر تاریخ‌ها شمسی نمی‌شوند:
1. Console browser را چک کنید برای خطاهای JavaScript
2. مطمئن شوید که فایل‌های JS/CSS به درستی لود شده‌اند
3. Cache را clear کنید: `bench --site [site-name] clear-cache`

### اگر Datepicker کار نمی‌کند:
1. مطمئن شوید که persianDatepicker files دانلود و در جای درست قرار گرفته‌اند
2. Browser console را برای خطاها چک کنید

## پشتیبانی

برای مشکلات و سوالات:
- Issue در GitHub بسازید
- در Forum ERPNext سوال بپرسید

## نکات مهم

- این App هیچ تغییری در Core ERPNext ایجاد نمی‌کند
- تمام تاریخ‌ها به صورت میلادی در دیتابیس ذخیره می‌شوند
- فقط نمایش و ورودی به صورت شمسی است
