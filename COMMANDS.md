# 📝 دستورات کامل Jalali Calendar

## 🚀 دستورات نصب

### نصب کامل از صفر
```bash
# 1. آماده‌سازی محیط
cd ~/frappe-bench
git clone https://github.com/yourusername/jalali_calendar apps/jalali_calendar

# 2. دادن permission به scripts
cd apps/jalali_calendar
chmod +x *.sh

# 3. نصب Python dependencies
pip install persiantools==3.0.1
pip install jdatetime==4.1.1

# 4. دانلود JavaScript dependencies
./download_dependencies.sh

# 5. نصب در site
bench --site [SITE_NAME] install-app jalali_calendar

# 6. Build assets
bench build --app jalali_calendar

# 7. Clear cache
bench --site [SITE_NAME] clear-cache

# 8. Restart
bench restart
```

### نصب خودکار (یک خط)
```bash
cd ~/frappe-bench && git clone https://github.com/yourusername/jalali_calendar apps/jalali_calendar && cd apps/jalali_calendar && chmod +x install_enhanced.sh && ./install_enhanced.sh
```

## 🔧 دستورات مدیریت

### بررسی وضعیت
```bash
# بررسی نصب
bench --site [SITE_NAME] list-apps | grep jalali_calendar

# بررسی در Python console
bench --site [SITE_NAME] console
>>> import jalali_calendar
>>> from jalali_calendar.jalali_calendar.api_enhanced import convert_to_jalali
>>> convert_to_jalali("2024-11-10")

# بررسی logs
bench --site [SITE_NAME] show-logs
tail -f logs/frappe.log | grep jalali

# بررسی JavaScript در browser
# F12 > Console
jalali_calendar.config.enabled
jalali_calendar.sync_convert_to_jalali("2024-11-10")
```

### به‌روزرسانی
```bash
# Pull تغییرات جدید
cd apps/jalali_calendar
git pull origin main

# نصب مجدد dependencies
pip install -r requirements.txt
./download_dependencies.sh

# Migrate
bench --site [SITE_NAME] migrate

# Build مجدد
bench build --app jalali_calendar

# Clear cache
bench --site [SITE_NAME] clear-cache

# Restart
bench restart
```

### Backup قبل از تغییرات
```bash
# Backup کامل site
bench --site [SITE_NAME] backup

# فقط backup از تنظیمات
bench --site [SITE_NAME] export-fixtures
```

## 🛠️ دستورات Development

### ساخت Custom Field از CLI
```bash
bench --site [SITE_NAME] console
>>> from frappe.custom.doctype.custom_field.custom_field import create_custom_field
>>> create_custom_field("User", {
...     "fieldname": "use_jalali_calendar",
...     "label": "استفاده از تقویم شمسی",
...     "fieldtype": "Check"
... })
```

### تست API
```bash
# Python API test
bench --site [SITE_NAME] execute jalali_calendar.jalali_calendar.api_enhanced.convert_to_jalali --args '["2024-11-10"]'

# REST API test
curl -X POST http://[SITE_URL]/api/method/jalali_calendar.jalali_calendar.api_enhanced.convert_to_jalali \
  -H "Authorization: token [API_KEY]:[API_SECRET]" \
  -H "Content-Type: application/json" \
  -d '{"gregorian_date": "2024-11-10"}'
```

### Debug mode
```bash
# فعال کردن debug mode
bench --site [SITE_NAME] set-config developer_mode 1

# مشاهده detailed logs
bench --site [SITE_NAME] set-config logging 2

# Console با auto-reload
bench --site [SITE_NAME] console --autoreload
```

## 🔄 دستورات Cache

### Clear different cache types
```bash
# Clear all cache
bench --site [SITE_NAME] clear-cache

# Clear specific cache
bench --site [SITE_NAME] console
>>> import frappe
>>> frappe.cache().delete_pattern("jalali_*")

# Clear user specific cache
>>> frappe.cache().hdel("user_permissions", "user@example.com")

# Clear website cache
bench --site [SITE_NAME] clear-website-cache
```

## 📊 دستورات Database

### Query تاریخ‌ها
```bash
bench --site [SITE_NAME] mariadb
> SELECT name, posting_date FROM `tabSales Invoice` WHERE posting_date >= '2024-01-01';

# تبدیل bulk تاریخ‌ها
bench --site [SITE_NAME] console
>>> import frappe
>>> from jalali_calendar.jalali_calendar.api_enhanced import convert_to_jalali
>>> invoices = frappe.get_all("Sales Invoice", fields=["name", "posting_date"])
>>> for inv in invoices:
...     jalali = convert_to_jalali(inv.posting_date)
...     print(f"{inv.name}: {jalali['date']}")
```

## 🐛 دستورات عیب‌یابی

### رفع مشکلات رایج
```bash
# مشکل: JavaScript files لود نمی‌شوند
bench build --force --app jalali_calendar
bench clear-cache

# مشکل: تاریخ‌ها تبدیل نمی‌شوند
bench --site [SITE_NAME] console
>>> frappe.db.get_single_value("Jalali Calendar Settings", "enabled")
>>> frappe.db.set_value("Jalali Calendar Settings", "Jalali Calendar Settings", "enabled", 1)

# مشکل: Permission denied
bench --site [SITE_NAME] add-user-permission --user [USER] --doctype "Jalali Calendar Settings"

# مشکل: Module not found
bench --site [SITE_NAME] reinstall-app jalali_calendar
```

### Reset به حالت اولیه
```bash
# حذف تنظیمات
bench --site [SITE_NAME] console
>>> frappe.delete_doc("Jalali Calendar Settings", ignore_permissions=True)

# حذف custom fields
>>> frappe.delete_doc("Custom Field", "User-use_jalali_calendar", force=True)

# نصب مجدد
bench --site [SITE_NAME] uninstall-app jalali_calendar --yes
bench --site [SITE_NAME] install-app jalali_calendar
```

## 🚫 دستورات حذف

### حذف کامل App
```bash
# 1. Backup اول
bench --site [SITE_NAME] backup

# 2. Uninstall از site
bench --site [SITE_NAME] uninstall-app jalali_calendar --yes

# 3. حذف فایل‌ها
rm -rf apps/jalali_calendar

# 4. حذف از apps.txt
nano sites/apps.txt
# Remove jalali_calendar line

# 5. Clear cache
bench --site [SITE_NAME] clear-cache

# 6. Restart
bench restart
```

## 📦 دستورات Export/Import

### Export تنظیمات
```bash
# Export settings as fixtures
bench --site [SITE_NAME] export-fixtures --app jalali_calendar

# Export specific DocType
bench --site [SITE_NAME] console
>>> from frappe.core.doctype.data_export.data_export import export_data
>>> export_data("Jalali Calendar Settings", "json")
```

### Import به site جدید
```bash
# کپی app به site جدید
cp -r apps/jalali_calendar ~/other-bench/apps/

# نصب در site جدید
cd ~/other-bench
bench --site [NEW_SITE] install-app jalali_calendar

# Import fixtures
bench --site [NEW_SITE] migrate
```

## 🔐 دستورات Security

### بررسی permissions
```bash
bench --site [SITE_NAME] console
>>> from frappe.permissions import get_roles
>>> get_roles("jalali_calendar.jalali_calendar.api_enhanced.convert_to_jalali")

# تنظیم permissions
>>> frappe.only_for("System Manager")
```

## 📈 دستورات Performance

### Monitor performance
```bash
# مشاهده slow queries
bench --site [SITE_NAME] mariadb-slow-queries

# Profile specific function
bench --site [SITE_NAME] console
>>> import cProfile
>>> cProfile.run('convert_to_jalali("2024-11-10")')

# Memory usage
>>> import tracemalloc
>>> tracemalloc.start()
>>> # run your code
>>> snapshot = tracemalloc.take_snapshot()
>>> top_stats = snapshot.statistics('lineno')
```

## 🎯 Shortcuts مفید

```bash
# Alias ها برای راحتی (اضافه به ~/.bashrc)
alias jc-install='bench --site [SITE_NAME] install-app jalali_calendar'
alias jc-build='bench build --app jalali_calendar'
alias jc-clear='bench --site [SITE_NAME] clear-cache'
alias jc-restart='bench restart'
alias jc-test='bench --site [SITE_NAME] console -c "from jalali_calendar.jalali_calendar.api_enhanced import convert_to_jalali; print(convert_to_jalali(\"2024-11-10\"))"'
```

---

**نکته:** جایگزین کنید `[SITE_NAME]` با نام واقعی site خودتان
