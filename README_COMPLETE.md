# 🗓️ Jalali Calendar for ERPNext 15

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ERPNext Version](https://img.shields.io/badge/ERPNext-v15-blue.svg)](https://erpnext.com)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org)

یک Custom App کامل و حرفه‌ای برای اضافه کردن تقویم شمسی (جلالی) به ERPNext بدون تغییر در Core

## ✨ ویژگی‌ها

- 📅 **تبدیل خودکار تاریخ‌ها** - نمایش شمسی، ذخیره میلادی
- 📊 **پشتیبانی کامل** - Forms, Lists, Reports, Print
- ⚡ **عملکرد بالا** - Cache و بهینه‌سازی
- 🎨 **قابل شخصی‌سازی** - تنظیمات کامل
- ⌨️ **میانبرهای کیبورد** - دسترسی سریع
- 🔒 **امن** - بدون تغییر در Core ERPNext

## 📋 پیش‌نیازها

- ERPNext 15 یا بالاتر
- Python 3.8+
- Node.js 14+
- Bench CLI

## 🚀 نصب سریع (Quick Install)

### روش 1: نصب خودکار (توصیه شده)

```bash
# 1. دانلود و آماده‌سازی
cd ~/frappe-bench
git clone https://github.com/yourusername/jalali_calendar apps/jalali_calendar
cd apps/jalali_calendar

# 2. اجازه اجرا به اسکریپت‌ها
chmod +x install_enhanced.sh
chmod +x download_dependencies.sh

# 3. دانلود وابستگی‌های خارجی
./download_dependencies.sh

# 4. نصب خودکار
./install_enhanced.sh
```

### روش 2: نصب دستی

```bash
# 1. Clone repository
cd ~/frappe-bench
git clone https://github.com/yourusername/jalali_calendar apps/jalali_calendar

# 2. نصب وابستگی‌های Python
pip install persiantools==3.0.1 jdatetime==4.1.1

# 3. دانلود JavaScript libraries
cd apps/jalali_calendar
./download_dependencies.sh

# 4. نصب App در Site
bench --site [your-site-name] install-app jalali_calendar

# 5. اجرای migrations
bench --site [your-site-name] migrate

# 6. Build assets
bench build --app jalali_calendar

# 7. Clear cache
bench --site [your-site-name] clear-cache

# 8. Restart services
bench restart
```

## 🔧 پیکربندی

### 1. تنظیمات سیستمی

```bash
# Login به ERPNext
# رفتن به:
Settings > Jalali Calendar Settings

# فعال‌سازی:
✅ فعال (Enabled)
✅ فعال در لیست‌ها
✅ فعال در گزارش‌ها
✅ فعال در چاپ
```

### 2. تنظیمات کاربر

```bash
# برای هر کاربر:
Users > [Select User] > Edit
✅ استفاده از تقویم شمسی
Save
```

## 📖 راهنمای استفاده

### در Forms
```python
# تایپ مستقیم تاریخ شمسی
Posting Date: 1403/08/20

# خودکار تبدیل می‌شود و ذخیره میلادی
Database: 2024-11-10
```

### در Reports
```python
# فیلتر با تاریخ شمسی
From Date: 1403/08/01
To Date: 1403/08/30
```

### Keyboard Shortcuts
| Shortcut | عملکرد |
|----------|--------|
| `Ctrl+Shift+T` | نمایش تاریخ امروز به شمسی |
| `Ctrl+Shift+J` | فعال/غیرفعال تقویم شمسی |
| `Ctrl+Shift+C` | نمایش تقویم ماه جاری |

## 🛠️ دستورات مفید

### بررسی وضعیت نصب
```bash
# لیست Apps نصب شده
bench --site [your-site] list-apps

# بررسی در Console
bench --site [your-site] console
>>> import jalali_calendar
>>> print("✅ Installed")
```

### عیب‌یابی
```bash
# Clear Cache
bench --site [your-site] clear-cache

# Rebuild
bench build --app jalali_calendar

# Restart
bench restart

# مشاهده Logs
bench --site [your-site] show-logs
```

### حذف App
```bash
# Uninstall از Site
bench --site [your-site] uninstall-app jalali_calendar

# حذف فایل‌ها
rm -rf apps/jalali_calendar
```

## 🔌 API Reference

### Python API
```python
from jalali_calendar.jalali_calendar.api_enhanced import convert_to_jalali

# تبدیل به شمسی
result = convert_to_jalali("2024-11-10")
# {'date': '1403/08/20', 'year': 1403, 'month': 8, 'day': 20}

# تبدیل به میلادی
from jalali_calendar.jalali_calendar.api_enhanced import convert_to_gregorian
result = convert_to_gregorian("1403/08/20")
# "2024-11-10"
```

### JavaScript API
```javascript
// تبدیل به شمسی
jalali_calendar.sync_convert_to_jalali('2024-11-10');
// Returns: "1403/08/20"

// تبدیل به میلادی
jalali_calendar.sync_convert_to_gregorian('1403/08/20');
// Returns: "2024-11-10"

// نمایش تقویم
jalali_calendar.show_month_calendar();
```

### REST API
```bash
# تبدیل به شمسی
curl -X POST http://your-site/api/method/jalali_calendar.jalali_calendar.api_enhanced.convert_to_jalali \
  -H "Content-Type: application/json" \
  -d '{"gregorian_date": "2024-11-10"}'

# دریافت تعطیلات
curl http://your-site/api/method/jalali_calendar.jalali_calendar.api_enhanced.get_holidays
```

### Jinja Templates
```jinja
<!-- در Print Format -->
{{ doc.posting_date | to_jalali }}
{{ doc.posting_date | to_jalali("long") }}
{{ doc.posting_date | jalali_format("DD MMMM YYYY") }}
```

## 📁 ساختار پروژه

```
jalali_calendar/
├── jalali_calendar/
│   ├── api_enhanced.py          # توابع API
│   ├── doctype/                 # DocTypes
│   ├── utils/                   # Utilities
│   ├── report_handler.py        # مدیریت گزارش‌ها
│   └── install.py               # اسکریپت نصب
├── public/
│   ├── js/                      # JavaScript files
│   └── css/                     # Stylesheets
├── LICENSE                      # MIT License
├── README.md                    # این فایل
└── requirements.txt             # Python dependencies
```

## 🤝 مشارکت

Pull requests پذیرفته می‌شوند! برای تغییرات بزرگ، لطفاً ابتدا issue باز کنید.

```bash
# Fork the repo
# Create your feature branch
git checkout -b feature/AmazingFeature

# Commit your changes
git commit -m 'Add some AmazingFeature'

# Push to the branch
git push origin feature/AmazingFeature

# Open a Pull Request
```

## 📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است - فایل [LICENSE](LICENSE) را ببینید.

### وابستگی‌های Third-Party:
- **Moment-Jalaali** - MIT License
- **PersianDatepicker** - MIT License
- **PersianTools** - MIT License
- **JDatetime** - BSD License
- **Vazir Font** - SIL Open Font License

## 🐛 گزارش مشکل

مشکلی پیدا کردید؟ لطفاً گزارش دهید:

1. [GitHub Issues](https://github.com/yourusername/jalali_calendar/issues)
2. Email: support@yourcompany.com
3. [ERPNext Forum](https://discuss.erpnext.com)

## 📞 پشتیبانی

- 📧 Email: support@yourcompany.com
- 💬 Telegram: @jalali_calendar_support
- 📖 [Documentation](DOCUMENTATION.md)
- 🎥 [Video Tutorial](https://youtube.com/...)

## 🙏 تشکر از

- تیم [Frappe/ERPNext](https://frappe.io)
- توسعه‌دهندگان [PersianTools](https://github.com/persian-tools)
- [Moment-Jalaali](https://github.com/jalaali/moment-jalaali) Contributors
- جامعه Open Source ایران

## ⭐ حمایت از پروژه

اگر این پروژه مفید بود، لطفاً:
- ⭐ ستاره بدهید
- 🍴 Fork کنید
- 🐛 Issue گزارش دهید
- 🔀 Pull Request بفرستید

---

ساخته شده با ❤️ برای جامعه ERPNext ایران

**نسخه:** 1.0.0  
**آخرین بروزرسانی:** 2024
