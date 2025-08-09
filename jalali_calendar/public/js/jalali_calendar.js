/**
 * Jalali Calendar Integration for ERPNext
 * نسخه 1.0.0
 */

frappe.provide('jalali_calendar');

// تنظیمات اولیه
jalali_calendar.config = {
    enabled: false,
    format: 'YYYY/MM/DD',
    months: [
        'فروردین', 'اردیبهشت', 'خرداد',
        'تیر', 'مرداد', 'شهریور',
        'مهر', 'آبان', 'آذر',
        'دی', 'بهمن', 'اسفند'
    ],
    weekDays: [
        'شنبه', 'یکشنبه', 'دوشنبه',
        'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه'
    ]
};

// بررسی فعال بودن تقویم شمسی برای کاربر
jalali_calendar.check_user_preference = function() {
    frappe.call({
        method: 'jalali_calendar.jalali_calendar.api.get_user_calendar_preference',
        callback: function(r) {
            if (r.message) {
                jalali_calendar.config.enabled = r.message;
                if (jalali_calendar.config.enabled) {
                    jalali_calendar.init();
                }
            }
        }
    });
};

// تابع اصلی برای شروع
jalali_calendar.init = function() {
    console.log('Jalali Calendar Initialized');
    
    // Override کردن frappe date controls
    jalali_calendar.override_date_controls();
    
    // اضافه کردن listener ها
    jalali_calendar.add_event_listeners();
};

// Override کردن Date Control
jalali_calendar.override_date_controls = function() {
    const original_make = frappe.ui.form.ControlDate.prototype.make;
    
    frappe.ui.form.ControlDate.prototype.make = function() {
        original_make.call(this);
        
        if (!jalali_calendar.config.enabled) {
            return;
        }
        
        const control = this;
        
        // تبدیل مقدار اولیه به شمسی
        if (control.value) {
            jalali_calendar.convert_and_display(control);
        }
        
        // Override set_input
        const original_set_input = control.set_input;
        control.set_input = function(value) {
            if (value && jalali_calendar.config.enabled) {
                // تبدیل میلادی به شمسی برای نمایش
                frappe.call({
                    method: 'jalali_calendar.jalali_calendar.api.convert_to_jalali',
                    args: {
                        gregorian_date: value
                    },
                    callback: function(r) {
                        if (r.message && r.message.date) {
                            control.$input.val(r.message.date);
                            control.$input.attr('data-gregorian', value);
                        } else {
                            original_set_input.call(control, value);
                        }
                    }
                });
            } else {
                original_set_input.call(control, value);
            }
        };
        
        // Override get_value
        const original_get_value = control.get_value;
        control.get_value = function() {
            if (jalali_calendar.config.enabled) {
                // اگر مقدار gregorian ذخیره شده باشد، آن را برگردان
                const gregorian = control.$input.attr('data-gregorian');
                if (gregorian) {
                    return gregorian;
                }
                
                // در غیر این صورت، تبدیل شمسی به میلادی
                const jalali_value = control.$input.val();
                if (jalali_value && jalali_value.includes('/')) {
                    // این یک تاریخ شمسی است، باید تبدیل شود
                    return jalali_calendar.sync_convert_to_gregorian(jalali_value);
                }
            }
            return original_get_value.call(control);
        };
    };
};

// تبدیل و نمایش تاریخ شمسی
jalali_calendar.convert_and_display = function(control) {
    if (!control.value) return;
    
    frappe.call({
        method: 'jalali_calendar.jalali_calendar.api.convert_to_jalali',
        args: {
            gregorian_date: control.value
        },
        callback: function(r) {
            if (r.message && r.message.date) {
                control.$input.val(r.message.date);
                control.$input.attr('data-gregorian', control.value);
            }
        }
    });
};

// تبدیل همزمان به میلادی (برای قبل از ذخیره)
jalali_calendar.sync_convert_to_gregorian = function(jalali_date) {
    let gregorian = jalali_date;
    
    frappe.call({
        method: 'jalali_calendar.jalali_calendar.api.convert_to_gregorian',
        args: {
            jalali_date_str: jalali_date
        },
        async: false,
        callback: function(r) {
            if (r.message) {
                gregorian = r.message;
            }
        }
    });
    
    return gregorian;
};

// اضافه کردن Event Listeners
jalali_calendar.add_event_listeners = function() {
    // Listen to form refresh events
    frappe.ui.form.on('*', {
        refresh: function(frm) {
            if (!jalali_calendar.config.enabled) return;
            
            // تبدیل تمام فیلدهای تاریخ به شمسی
            jalali_calendar.convert_form_dates(frm);
        },
        
        before_save: function(frm) {
            if (!jalali_calendar.config.enabled) return;
            
            // تبدیل تاریخ‌های شمسی به میلادی قبل از ذخیره
            jalali_calendar.convert_dates_before_save(frm);
        }
    });
};

// تبدیل تاریخ‌های فرم به شمسی
jalali_calendar.convert_form_dates = function(frm) {
    const date_fields = frm.meta.fields.filter(
        field => field.fieldtype === 'Date' || field.fieldtype === 'Datetime'
    );
    
    date_fields.forEach(field => {
        const control = frm.fields_dict[field.fieldname];
        if (control && control.value) {
            jalali_calendar.convert_and_display(control);
        }
    });
};

// تبدیل تاریخ‌ها قبل از ذخیره
jalali_calendar.convert_dates_before_save = function(frm) {
    const date_fields = frm.meta.fields.filter(
        field => field.fieldtype === 'Date' || field.fieldtype === 'Datetime'
    );
    
    date_fields.forEach(field => {
        const control = frm.fields_dict[field.fieldname];
        if (control && control.$input) {
            const jalali_value = control.$input.val();
            const gregorian_value = control.$input.attr('data-gregorian');
            
            if (gregorian_value) {
                // استفاده از مقدار میلادی ذخیره شده
                frm.doc[field.fieldname] = gregorian_value;
            } else if (jalali_value && jalali_value.includes('/')) {
                // تبدیل شمسی به میلادی
                const gregorian = jalali_calendar.sync_convert_to_gregorian(jalali_value);
                frm.doc[field.fieldname] = gregorian;
            }
        }
    });
};

// اضافه کردن datepicker شمسی
jalali_calendar.setup_persian_datepicker = function(input_element) {
    if (typeof $.fn.persianDatepicker !== 'undefined') {
        $(input_element).persianDatepicker({
            months: jalali_calendar.config.months,
            dowTitle: jalali_calendar.config.weekDays,
            shortDowTitle: ['ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج'],
            persianNumbers: true,
            formatDate: "YYYY/MM/DD",
            onSelect: function() {
                const selected_date = $(input_element).val();
                // تبدیل به میلادی و ذخیره
                frappe.call({
                    method: 'jalali_calendar.jalali_calendar.api.convert_to_gregorian',
                    args: {
                        jalali_date_str: selected_date
                    },
                    callback: function(r) {
                        if (r.message) {
                            $(input_element).attr('data-gregorian', r.message);
                            $(input_element).trigger('change');
                        }
                    }
                });
            }
        });
    }
};

// تنظیمات List View
jalali_calendar.setup_list_view = function() {
    if (!jalali_calendar.config.enabled) return;
    
    // Override list view formatters
    frappe.listview_settings = frappe.listview_settings || {};
    
    // برای همه DocTypes
    const original_get_indicator = frappe.listview_settings.get_indicator;
    
    frappe.listview_settings.get_indicator = function(doc) {
        // تبدیل تاریخ‌ها در list view
        jalali_calendar.convert_doc_dates_in_list(doc);
        
        if (original_get_indicator) {
            return original_get_indicator.call(this, doc);
        }
    };
    
    // Override date formatter
    frappe.datetime.str_to_user = function(date_str) {
        if (!date_str || !jalali_calendar.config.enabled) {
            return frappe.datetime.str_to_user_old ? 
                   frappe.datetime.str_to_user_old(date_str) : date_str;
        }
        
        // تبدیل به شمسی برای نمایش
        let jalali_date = '';
        frappe.call({
            method: 'jalali_calendar.jalali_calendar.api.convert_to_jalali',
            args: { gregorian_date: date_str },
            async: false,
            callback: function(r) {
                if (r.message && r.message.date) {
                    jalali_date = r.message.date;
                }
            }
        });
        
        return jalali_date || date_str;
    };
};

// تبدیل تاریخ‌ها در یک سند در list view
jalali_calendar.convert_doc_dates_in_list = function(doc) {
    if (!jalali_calendar.config.enabled) return;
    
    // فیلدهای تاریخ رایج
    const date_fields = ['creation', 'modified', 'posting_date', 'transaction_date', 
                        'due_date', 'delivery_date', 'from_date', 'to_date'];
    
    date_fields.forEach(field => {
        if (doc[field]) {
            doc[field + '_jalali'] = jalali_calendar.quick_convert_to_jalali(doc[field]);
        }
    });
};

// تبدیل سریع برای استفاده در list view
jalali_calendar.quick_convert_to_jalali = function(date_str) {
    if (!date_str) return '';
    
    // استفاده از cache برای performance
    if (jalali_calendar._cache && jalali_calendar._cache[date_str]) {
        return jalali_calendar._cache[date_str];
    }
    
    let result = '';
    frappe.call({
        method: 'jalali_calendar.jalali_calendar.api.convert_to_jalali',
        args: { gregorian_date: date_str },
        async: false,
        callback: function(r) {
            if (r.message && r.message.date) {
                result = r.message.date;
                // ذخیره در cache
                if (!jalali_calendar._cache) jalali_calendar._cache = {};
                jalali_calendar._cache[date_str] = result;
            }
        }
    });
    
    return result;
};

// Calendar Widget شمسی
jalali_calendar.create_calendar_widget = function(wrapper) {
    if (!jalali_calendar.config.enabled) return;
    
    const today = new Date();
    frappe.call({
        method: 'jalali_calendar.jalali_calendar.api.get_jalali_calendar_data',
        args: {
            year: today.getFullYear(),
            month: today.getMonth() + 1
        },
        callback: function(r) {
            if (r.message) {
                jalali_calendar.render_calendar(wrapper, r.message);
            }
        }
    });
};

// رندر تقویم شمسی
jalali_calendar.render_calendar = function(wrapper, data) {
    const calendar_html = `
        <div class="jalali-calendar-widget">
            <div class="calendar-header">
                <button class="prev-month">❮</button>
                <h3>${data.month_name} ${data.year}</h3>
                <button class="next-month">❯</button>
            </div>
            <div class="calendar-grid">
                ${jalali_calendar.generate_calendar_grid(data)}
            </div>
        </div>
    `;
    
    $(wrapper).html(calendar_html);
    jalali_calendar.bind_calendar_events(wrapper);
};

// Date Range Picker شمسی
jalali_calendar.setup_range_picker = function(from_field, to_field) {
    if (!jalali_calendar.config.enabled) return;
    
    const $from = $(from_field);
    const $to = $(to_field);
    
    $from.on('change', function() {
        const from_date = $(this).val();
        if (from_date) {
            $to.attr('min', from_date);
        }
    });
    
    $to.on('change', function() {
        const to_date = $(this).val();
        if (to_date) {
            $from.attr('max', to_date);
        }
    });
};

// Keyboard Shortcuts
jalali_calendar.setup_keyboard_shortcuts = function() {
    // تاریخ امروز به شمسی
    frappe.ui.keys.add_shortcut({
        shortcut: 'ctrl+shift+t',
        action: () => {
            frappe.call({
                method: 'jalali_calendar.jalali_calendar.api.get_today_jalali',
                callback: function(r) {
                    if (r.message) {
                        frappe.show_alert({
                            message: `امروز: ${r.message.date}`,
                            indicator: 'green'
                        });
                    }
                }
            });
        },
        description: 'نمایش تاریخ امروز به شمسی'
    });
    
    // تبدیل سریع تاریخ
    frappe.ui.keys.add_shortcut({
        shortcut: 'ctrl+shift+c',
        action: () => {
            jalali_calendar.show_quick_converter();
        },
        description: 'تبدیل سریع تاریخ'
    });
};

// نمایش تبدیل‌گر سریع
jalali_calendar.show_quick_converter = function() {
    const d = new frappe.ui.Dialog({
        title: 'تبدیل تاریخ',
        fields: [
            {
                label: 'تاریخ میلادی',
                fieldname: 'gregorian_date',
                fieldtype: 'Date',
                onchange: function() {
                    const greg_date = this.get_value();
                    if (greg_date) {
                        frappe.call({
                            method: 'jalali_calendar.jalali_calendar.api.convert_to_jalali',
                            args: { gregorian_date: greg_date },
                            callback: function(r) {
                                if (r.message) {
                                    d.set_value('jalali_date', r.message.date);
                                }
                            }
                        });
                    }
                }
            },
            {
                label: 'تاریخ شمسی',
                fieldname: 'jalali_date',
                fieldtype: 'Data',
                onchange: function() {
                    const jalali_date = this.get_value();
                    if (jalali_date) {
                        frappe.call({
                            method: 'jalali_calendar.jalali_calendar.api.convert_to_gregorian',
                            args: { jalali_date_str: jalali_date },
                            callback: function(r) {
                                if (r.message) {
                                    d.set_value('gregorian_date', r.message);
                                }
                            }
                        });
                    }
                }
            }
        ],
        primary_action_label: 'بستن',
        primary_action(values) {
            d.hide();
        }
    });
    
    d.show();
};

// شروع اتوماتیک بعد از لود صفحه
$(document).ready(function() {
    jalali_calendar.check_user_preference();
    
    // Setup additional features
    setTimeout(() => {
        if (jalali_calendar.config.enabled) {
            jalali_calendar.setup_list_view();
            jalali_calendar.setup_keyboard_shortcuts();
        }
    }, 1000);
});

// Export for global access
window.jalali_calendar = jalali_calendar;
