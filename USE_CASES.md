# 🔄 سناریوهای کاربردی Jalali Calendar

## سناریو 1: ثبت حسابداری روزانه

### مراحل:
1. **ایجاد Journal Entry**
   ```
   Accounting > Journal Entry > New
   ```

2. **تنظیم تاریخ:**
   - Posting Date: تایپ کنید `1403/08/20`
   - یا کلیک روی آیکون تقویم و انتخاب از تقویم شمسی

3. **وارد کردن اقلام:**
   - حساب‌ها و مبالغ را وارد کنید
   - Reference Date هم به شمسی قابل ورود است

4. **Save & Submit:**
   - تاریخ‌ها به میلادی تبدیل و ذخیره می‌شوند
   - در View همچنان شمسی نمایش داده می‌شوند

---

## سناریو 2: گزارش‌گیری ماهانه

### گزارش فروش ماه جاری:
1. **Sales Register**
   ```
   Selling > Reports > Sales Register
   ```

2. **تنظیم فیلترها:**
   ```
   From Date: 1403/08/01
   To Date: 1403/08/30
   Company: Your Company
   ```

3. **Export:**
   - Excel: کلیک روی Export > Excel
   - تمام تاریخ‌ها در Excel به شمسی خواهند بود

---

## سناریو 3: جستجوی تاریخی

### جستجوی فاکتورهای یک روز خاص:
1. **در List View فاکتورها:**
   ```
   Sales Invoice List
   ```

2. **استفاده از Filters:**
   - Add Filter
   - Field: Posting Date
   - Condition: Equals
   - Value: `1403/07/15`

3. **نتیجه:**
   - سیستم به میلادی تبدیل می‌کند
   - Query را اجرا می‌کند
   - نتایج را با تاریخ شمسی نشان می‌دهد

---

## سناریو 4: برنامه‌ریزی با تقویم

### تنظیم یادآوری:
1. **ایجاد Task:**
   ```
   Projects > Task > New
   ```

2. **تاریخ‌ها:**
   ```
   Expected Start Date: 1403/09/01
   Expected End Date: 1403/09/15
   ```

3. **در Calendar View:**
   - تسک‌ها با تاریخ شمسی نمایش داده می‌شوند
   - Drag & Drop با حفظ تبدیل صحیح

---

## سناریو 5: Import/Export با Excel

### Import داده با تاریخ شمسی:
1. **آماده‌سازی Excel:**
   ```
   | Item    | Date       | Amount |
   |---------|------------|--------|
   | Item-1  | 1403/08/15 | 1000   |
   | Item-2  | 1403/08/16 | 2000   |
   ```

2. **Import:**
   ```
   Data Import > New
   Select DocType > Upload File
   ```

3. **نتیجه:**
   - اگر "تبدیل خودکار در Import" فعال باشد
   - تاریخ‌ها به میلادی تبدیل می‌شوند
   - در دیتابیس صحیح ذخیره می‌شوند

---

## سناریو 6: استفاده در Custom Scripts

### Client Script برای فرم:
```javascript
frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        // دریافت تاریخ امروز به شمسی
        frappe.call({
            method: 'jalali_calendar.jalali_calendar.api_enhanced.convert_to_jalali',
            args: {
                gregorian_date: frappe.datetime.now_date()
            },
            callback: function(r) {
                if(r.message) {
                    frm.set_intro(`امروز: ${r.message.formatted_long}`);
                }
            }
        });
    },
    
    posting_date: function(frm) {
        // اعتبارسنجی تاریخ شمسی
        if(frm.doc.posting_date && frm.doc.posting_date.includes('/')) {
            frappe.call({
                method: 'jalali_calendar.jalali_calendar.api_enhanced.validate_jalali_date',
                args: {
                    jalali_date_str: frm.doc.posting_date
                },
                callback: function(r) {
                    if(r.message && !r.message.valid) {
                        frappe.msgprint({
                            title: 'خطا در تاریخ',
                            message: r.message.error,
                            indicator: 'red'
                        });
                    }
                }
            });
        }
    }
});
```

---

## سناریو 7: تنظیم تعطیلات

### اضافه کردن تعطیلات جدید:
1. **Jalali Calendar Settings**
2. **در جدول تعطیلات:**
   ```
   Date: 22/11
   Title: پیروزی انقلاب
   Recurring: ✓
   ```
3. **Save**

### نتیجه:
- هر سال در این تاریخ
- Notification برای کاربران
- نمایش در تقویم

---

## سناریو 8: گزارش سفارشی با Jinja

### در Print Format سفارشی:
```html
<div class="print-heading">
    <h2>فاکتور فروش</h2>
</div>

<div class="row">
    <div class="col-xs-6">
        <!-- تاریخ کوتاه -->
        <strong>تاریخ:</strong> {{ doc.posting_date | to_jalali }}
    </div>
    <div class="col-xs-6">
        <!-- تاریخ بلند -->
        <strong>سررسید:</strong> {{ doc.due_date | to_jalali("long") }}
    </div>
</div>

<div class="row">
    <!-- تاریخ با فرمت دلخواه -->
    <strong>تاریخ چاپ:</strong> 
    {{ frappe.utils.now() | jalali_format("DD MMMM YYYY ساعت HH:mm") }}
</div>
```
