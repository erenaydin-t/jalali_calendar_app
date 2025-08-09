# 📅 Jalali Calendar for ERPNext - Complete Documentation

## فهرست مطالب
1. [معرفی](#معرفی)
2. [ویژگی‌ها](#ویژگی‌ها)
3. [نصب](#نصب)
4. [پیکربندی](#پیکربندی)
5. [استفاده](#استفاده)
6. [API Reference](#api-reference)
7. [عیب‌یابی](#عیب‌یابی)
8. [توسعه](#توسعه)

## معرفی

Jalali Calendar یک Custom App کامل برای ERPNext 15 است که قابلیت تقویم شمسی (جلالی) را به سیستم اضافه می‌کند بدون نیاز به تغییر در هسته ERPNext.

### مزایا
- ✅ بدون تغییر Core ERPNext
- ✅ ذخیره‌سازی میلادی در دیتابیس
- ✅ نمایش و ورودی شمسی
- ✅ پشتیبانی از List View, Reports, Print
- ✅ Keyboard Shortcuts
- ✅ User/System Settings

## ویژگی‌ها

### 🎯 ویژگی‌های اصلی
1. **تبدیل خودکار تاریخ‌ها**
   - نمایش شمسی در فرم‌ها
   - ذخیره میلادی در دیتابیس
   - تبدیل دوطرفه بدون خطا

2. **پشتیبانی کامل از Views**
   - ✅ Form View
   - ✅ List View
   - ✅ Report View
   - ✅ Print Format
   - ✅ Calendar View

3. **تنظیمات پیشرفته**
   - Settings Page مخصوص
   - User Preferences
   - System-wide Settings
   - Holiday Management

4. **Keyboard Shortcuts**
   - `Ctrl+Shift+T`: تاریخ امروز
   - `Ctrl+Shift+J`: Toggle تقویم
   - `Ctrl+Shift+C`: نمایش تقویم ماه

5. **API کامل**
   - REST API endpoints
   - Jinja filters
   - Python API
   - JavaScript API

## نصب

### پیش‌نیازها
```bash
- ERPNext 15+
- Python 3.8+
- Node.js 14+
```

### نصب خودکار
```bash
cd frappe-bench
chmod +x install_enhanced.sh
./install_enhanced.sh
```

### نصب دستی
```bash
# 1. Clone repository
cd frappe-bench/apps
git clone https://github.com/yourusername/jalali_calendar

# 2. Install Python dependencies
pip install persiantools jdatetime

# 3. Install app
bench --site your-site install-app jalali_calendar

# 4. Build assets
bench build --app jalali_calendar

# 5. Clear cache & restart
bench clear-cache
bench restart
```

## پیکربندی

### 1. تنظیمات سیستمی
```
Settings > Jalali Calendar Settings
```

#### فیلدهای اصلی:
- **فعال**: روشن/خاموش کردن کل سیستم
- **برای همه کاربران**: اعمال برای تمام کاربران
- **فرمت تاریخ**: YYYY/MM/DD یا فرمت‌های دیگر
- **نمایش تعطیلات**: نمایش تعطیلات رسمی

### 2. تنظیمات کاربر
```
User > [Select User] > استفاده از تقویم شمسی
```

### 3. تعطیلات رسمی
در Settings می‌توانید تعطیلات را مدیریت کنید:
```python
{
    "date": "01/01",
    "title": "عید نوروز",
    "recurring": true
}
```

## استفاده

### در Forms
تمام فیلدهای Date/Datetime به صورت خودکار:
- **نمایش**: به شمسی
- **ورودی**: شمسی قابل قبول
- **ذخیره**: تبدیل به میلادی

### در Reports
فیلترها و نتایج به صورت شمسی:
```javascript
// فیلتر با تاریخ شمسی
filters: {
    from_date: "1403/01/01",
    to_date: "1403/01/31"
}
```

### در Print Format
استفاده از Jinja filters:
```jinja
<!-- تاریخ کوتاه -->
{{ doc.posting_date | to_jalali }}

<!-- تاریخ بلند -->
{{ doc.posting_date | to_jalali("long") }}

<!-- فرمت دلخواه -->
{{ doc.posting_date | jalali_format("DD MMMM YYYY") }}
```

### در Custom Scripts
```javascript
// تبدیل به شمسی
frappe.call({
    method: 'jalali_calendar.jalali_calendar.api_enhanced.convert_to_jalali',
    args: { gregorian_date: '2024-01-15' },
    callback: function(r) {
        console.log(r.message.date); // 1402/10/25
    }
});

// تبدیل به میلادی
jalali_calendar.sync_convert_to_gregorian('1402/10/25');
```

## API Reference

### Python API

#### `convert_to_jalali(gregorian_date)`
```python
from jalali_calendar.jalali_calendar.api_enhanced import convert_to_jalali

result = convert_to_jalali("2024-01-15")
# Returns: {
#     'date': '1402/10/25',
#     'year': 1402,
#     'month': 10,
#     'day': 25,
#     'month_name': 'دی'
# }
```

#### `convert_to_gregorian(jalali_date_str)`
```python
from jalali_calendar.jalali_calendar.api_enhanced import convert_to_gregorian

result = convert_to_gregorian("1402/10/25")
# Returns: "2024-01-15"
```

#### `validate_jalali_date(jalali_date_str)`
```python
result = validate_jalali_date("1402/13/01")
# Returns: {"valid": False, "error": "ماه باید بین 1 تا 12 باشد"}
```

### JavaScript API

#### تبدیل تاریخ
```javascript
// به شمسی
jalali_calendar.sync_convert_to_jalali('2024-01-15');

// به میلادی
jalali_calendar.sync_convert_to_gregorian('1402/10/25');
```

#### نمایش تقویم
```javascript
// تقویم ماه
jalali_calendar.show_month_calendar();

// Range Picker
jalali_calendar.show_range_picker(function(from, to) {
    console.log('Selected range:', from, to);
});
```

### REST API

#### Endpoints
```
POST /api/method/jalali_calendar.jalali_calendar.api_enhanced.convert_to_jalali
POST /api/method/jalali_calendar.jalali_calendar.api_enhanced.convert_to_gregorian
GET  /api/method/jalali_calendar.jalali_calendar.api_enhanced.get_holidays
```

## عیب‌یابی

### تاریخ‌ها نمایش داده نمی‌شوند
1. بررسی Console برای خطاهای JavaScript
2. بررسی فعال بودن در Settings
3. Clear cache: `bench clear-cache`

### Datepicker کار نمی‌کند
1. بررسی لود شدن فایل‌های JS/CSS
2. بررسی وجود فایل persianDatepicker.min.js

### تبدیل اشتباه
1. بررسی فرمت تاریخ ورودی
2. استفاده از validate_jalali_date
3. بررسی logs: `bench --site your-site console`

## توسعه

### ساختار پروژه
```
jalali_calendar/
├── jalali_calendar/
│   ├── api_enhanced.py          # API functions
│   ├── doctype/                 # DocTypes
│   │   ├── jalali_calendar_settings/
│   │   └── jalali_holiday/
│   ├── utils/
│   │   ├── date_converter.py    # Date conversion
│   │   ├── print_handler.py     # Print handling
│   │   └── jinja_filters.py     # Template filters
│   ├── report_handler.py        # Report integration
│   ├── tasks.py                 # Scheduled tasks
│   └── install.py               # Installation scripts
├── public/
│   ├── js/
│   │   └── jalali_calendar_enhanced.js
│   └── css/
│       └── jalali_calendar.css
└── hooks_enhanced.py            # App hooks
```

### اضافه کردن قابلیت جدید

#### 1. Backend (Python)
```python
# در api_enhanced.py
@frappe.whitelist()
def your_new_function(param):
    # Your code here
    return result
```

#### 2. Frontend (JavaScript)
```javascript
// در jalali_calendar_enhanced.js
jalali_calendar.your_feature = function() {
    // Your code here
};
```

#### 3. Hook جدید
```python
# در hooks_enhanced.py
doc_events = {
    "Your DocType": {
        "your_event": "jalali_calendar.path.to.handler"
    }
}
```

## مشارکت

Pull requests are welcome! برای تغییرات بزرگ، لطفاً ابتدا issue باز کنید.

## لایسنس

MIT License - استفاده آزاد برای پروژه‌های شخصی و تجاری

برای جزئیات کامل، فایل [LICENSE](LICENSE) را مشاهده کنید.

### Third-Party Libraries:
- Moment-Jalaali (MIT)
- PersianDatepicker (MIT)
- PersianTools (MIT)
- JDatetime (BSD)
- Vazir Font (SIL Open Font License)

## پشتیبانی

- 📧 Email: support@yourcompany.com
- 💬 Forum: discuss.erpnext.com
- 🐛 Issues: GitHub Issues

## تشکر از

- تیم Frappe/ERPNext
- توسعه‌دهندگان persiantools
- جامعه Open Source ایران

---

ساخته شده با ❤️ برای جامعه ERPNext ایران
