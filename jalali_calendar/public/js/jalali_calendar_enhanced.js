/**
 * Jalali Calendar Integration for ERPNext - Enhanced Version
 * نسخه پیشرفته با پشتیبانی کامل
 */

frappe.provide('jalali_calendar');

// تنظیمات اولیه
jalali_calendar.config = {
    enabled: false,
    format: 'YYYY/MM/DD',
    format_long: 'DD MMMM YYYY',
    show_holidays: true,
    first_day_of_week: 6, // شنبه
    months: [
        'فروردین', 'اردیبهشت', 'خرداد',
        'تیر', 'مرداد', 'شهریور',
        'مهر', 'آبان', 'آذر',
        'دی', 'بهمن', 'اسفند'
    ],
    weekDays: [
        'شنبه', 'یکشنبه', 'دوشنبه',
        'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه'
    ],
    shortWeekDays: ['ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج']
};

// =============== CORE FUNCTIONS ===============

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
    console.log('🗓️ Jalali Calendar Enhanced - Initialized');
    
    // Override کردن frappe date controls
    jalali_calendar.override_date_controls();
    
    // اضافه کردن listener ها
    jalali_calendar.add_event_listeners();
    
    // Setup list view
    jalali_calendar.setup_list_view();
    
    // Setup keyboard shortcuts
    jalali_calendar.setup_keyboard_shortcuts();
    
    // Setup report integration
    jalali_calendar.setup_report_integration();
    
    // Add calendar widget to navbar
    jalali_calendar.add_navbar_widget();
    
    // Initialize range picker
    jalali_calendar.init_range_picker();
};

// =============== DATE CONTROL OVERRIDES ===============

jalali_calendar.override_date_controls = function() {
    const original_make = frappe.ui.form.ControlDate.prototype.make;
    
    frappe.ui.form.ControlDate.prototype.make = function() {
        original_make.call(this);
        
        if (!jalali_calendar.config.enabled) {
            return;
        }
        
        const control = this;
        
        // Add jalali class
        control.$input.addClass('jalali-enabled');
        
        // تبدیل مقدار اولیه به شمسی
        if (control.value) {
            jalali_calendar.convert_and_display(control);
        }
        
        // Add calendar icon
        jalali_calendar.add_calendar_icon(control);
        
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
                            control.$input.attr('title', `میلادی: ${value}`);
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
                    return jalali_calendar.sync_convert_to_gregorian(jalali_value);
                }
            }
            return original_get_value.call(control);
        };
    };
};

// =============== LIST VIEW SUPPORT ===============

jalali_calendar.setup_list_view = function() {
    if (!jalali_calendar.config.enabled) return;
    
    // Override list formatters
    frappe.listview_settings = frappe.listview_settings || {};
    
    // Monitor DOM changes for list rows
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                mutation.addedNodes.forEach(function(node) {
                    if ($(node).hasClass('list-row') || $(node).find('.list-row').length) {
                        setTimeout(() => jalali_calendar.convert_list_dates(node), 100);
                    }
                });
            }
        });
    });
    
    // Start observing
    if (document.querySelector('.list-body')) {
        observer.observe(document.querySelector('.list-body'), {
            childList: true,
            subtree: true
        });
    }
    
    // Override date formatter
    const original_formatter = frappe.format;
    frappe.format = function(value, df, options, doc) {
        if (jalali_calendar.config.enabled && df && (df.fieldtype === 'Date' || df.fieldtype === 'Datetime')) {
            if (value) {
                const jalali = jalali_calendar.sync_convert_to_jalali(value);
                if (jalali) {
                    return `<span class="jalali-date list-jalali" title="${value}">${jalali}</span>`;
                }
            }
        }
        return original_formatter(value, df, options, doc);
    };
};

// تبدیل تاریخ‌ها در list row
jalali_calendar.convert_list_dates = function(container) {
    $(container).find('.list-row-col').each(function() {
        const $col = $(this);
        const text = $col.text().trim();
        
        // Check if it's a date format (YYYY-MM-DD)
        if (/^\d{4}-\d{2}-\d{2}/.test(text) && !$col.hasClass('jalali-converted')) {
            frappe.call({
                method: 'jalali_calendar.jalali_calendar.api.convert_to_jalali',
                args: { gregorian_date: text },
                callback: function(r) {
                    if (r.message && r.message.date) {
                        $col.html(`<span class="jalali-date" title="${text}">${r.message.date}</span>`);
                        $col.addClass('jalali-converted');
                    }
                }
            });
        }
    });
};

// =============== REPORT INTEGRATION ===============

jalali_calendar.setup_report_integration = function() {
    if (!jalali_calendar.config.enabled) return;
    
    // Override report date filters
    frappe.query_report_filters_by_name = frappe.query_report_filters_by_name || {};
    
    $(document).on('frappe.query_report.loaded', function() {
        // Convert date filters in reports
        if (frappe.query_report && frappe.query_report.filters) {
            frappe.query_report.filters.forEach(function(filter) {
                if (filter.df.fieldtype === 'Date' || filter.df.fieldtype === 'DateRange') {
                    jalali_calendar.setup_report_date_filter(filter);
                }
            });
        }
    });
};

// Setup report date filter
jalali_calendar.setup_report_date_filter = function(filter) {
    if (filter.$input) {
        filter.$input.addClass('jalali-enabled');
        
        // Add conversion logic
        const original_set_value = filter.set_value;
        filter.set_value = function(value) {
            if (value && jalali_calendar.config.enabled) {
                // Convert and display
                frappe.call({
                    method: 'jalali_calendar.jalali_calendar.api.convert_to_jalali',
                    args: { gregorian_date: value },
                    callback: function(r) {
                        if (r.message && r.message.date) {
                            filter.$input.val(r.message.date);
                            filter.$input.attr('data-gregorian', value);
                        }
                    }
                });
            }
            original_set_value.call(filter, value);
        };
    }
};

// =============== KEYBOARD SHORTCUTS ===============

jalali_calendar.setup_keyboard_shortcuts = function() {
    // نمایش تاریخ امروز
    frappe.ui.keys.add_shortcut({
        shortcut: 'ctrl+shift+t',
        action: () => {
            jalali_calendar.show_today_jalali();
        },
        description: 'نمایش تاریخ امروز به شمسی',
        ignore_inputs: true,
        page: undefined
    });
    
    // تغییر وضعیت تقویم
    frappe.ui.keys.add_shortcut({
        shortcut: 'ctrl+shift+j',
        action: () => {
            jalali_calendar.toggle_calendar();
        },
        description: 'تغییر وضعیت تقویم شمسی',
        ignore_inputs: true,
        page: undefined
    });
    
    // نمایش تقویم ماه جاری
    frappe.ui.keys.add_shortcut({
        shortcut: 'ctrl+shift+c',
        action: () => {
            jalali_calendar.show_month_calendar();
        },
        description: 'نمایش تقویم ماه جاری',
        ignore_inputs: true,
        page: undefined
    });
};

// =============== CALENDAR WIDGET ===============

jalali_calendar.add_navbar_widget = function() {
    if (!$('#navbar-jalali-date').length) {
        const today = new Date();
        frappe.call({
            method: 'jalali_calendar.jalali_calendar.api.convert_to_jalali',
            args: { gregorian_date: frappe.datetime.now_date() },
            callback: function(r) {
                if (r.message) {
                    const widget = `
                        <li id="navbar-jalali-date" class="nav-item dropdown">
                            <a class="nav-link" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                <span class="jalali-indicator">شمسی</span>
                                <span id="navbar-jalali-text">${r.message.date}</span>
                            </a>
                            <div class="dropdown-menu dropdown-menu-right" id="jalali-dropdown">
                                <div class="dropdown-item-text">
                                    <strong>${r.message.day} ${r.message.month_name} ${r.message.year}</strong>
                                </div>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item" onclick="jalali_calendar.show_month_calendar()">
                                    <i class="fa fa-calendar"></i> نمایش تقویم ماه
                                </a>
                                <a class="dropdown-item" onclick="jalali_calendar.open_settings()">
                                    <i class="fa fa-cog"></i> تنظیمات تقویم
                                </a>
                            </div>
                        </li>
                    `;
                    $('.navbar-nav.navbar-right').prepend(widget);
                }
            }
        });
    }
};

// =============== DATE RANGE PICKER ===============

jalali_calendar.init_range_picker = function() {
    jalali_calendar.range_picker = {
        from: null,
        to: null,
        callback: null
    };
};

jalali_calendar.show_range_picker = function(callback) {
    const d = new frappe.ui.Dialog({
        title: 'انتخاب بازه تاریخی',
        fields: [
            {
                label: 'از تاریخ',
                fieldname: 'from_date',
                fieldtype: 'Date',
                reqd: 1
            },
            {
                label: 'تا تاریخ',
                fieldname: 'to_date',
                fieldtype: 'Date',
                reqd: 1
            }
        ],
        primary_action_label: 'تایید',
        primary_action(values) {
            if (callback) {
                callback(values.from_date, values.to_date);
            }
            d.hide();
        }
    });
    
    d.show();
};

// =============== HELPER FUNCTIONS ===============

// نمایش تاریخ امروز
jalali_calendar.show_today_jalali = function() {
    const today = frappe.datetime.now_date();
    frappe.call({
        method: 'jalali_calendar.jalali_calendar.api.convert_to_jalali',
        args: { gregorian_date: today },
        callback: function(r) {
            if (r.message) {
                frappe.msgprint({
                    title: 'تاریخ امروز',
                    message: `
                        <div style="text-align: center; font-size: 18px;">
                            <strong>${r.message.day} ${r.message.month_name} ${r.message.year}</strong>
                            <br>
                            <span style="color: #666; font-size: 14px;">معادل: ${today}</span>
                        </div>
                    `,
                    indicator: 'green'
                });
            }
        }
    });
};

// تغییر وضعیت تقویم
jalali_calendar.toggle_calendar = function() {
    frappe.call({
        method: 'jalali_calendar.jalali_calendar.api.toggle_user_calendar',
        callback: function(r) {
            if (r.message !== undefined) {
                jalali_calendar.config.enabled = r.message;
                const status = r.message ? 'فعال' : 'غیرفعال';
                frappe.show_alert({
                    message: `تقویم شمسی ${status} شد`,
                    indicator: r.message ? 'green' : 'orange'
                }, 3);
                
                // Reload page to apply changes
                setTimeout(() => location.reload(), 1000);
            }
        }
    });
};

// نمایش تقویم ماه
jalali_calendar.show_month_calendar = function() {
    frappe.call({
        method: 'jalali_calendar.jalali_calendar.api.get_month_calendar',
        callback: function(r) {
            if (r.message) {
                const d = new frappe.ui.Dialog({
                    title: 'تقویم ماه جاری',
                    size: 'large'
                });
                
                d.$body.html(r.message);
                d.show();
            }
        }
    });
};

// باز کردن تنظیمات
jalali_calendar.open_settings = function() {
    frappe.set_route('Form', 'Jalali Calendar Settings');
};

// اضافه کردن آیکون تقویم
jalali_calendar.add_calendar_icon = function(control) {
    if (!control.$wrapper.find('.jalali-calendar-icon').length) {
        const icon = $('<i class="fa fa-calendar jalali-calendar-icon"></i>');
        icon.on('click', function() {
            jalali_calendar.show_persian_datepicker(control);
        });
        control.$wrapper.css('position', 'relative');
        control.$wrapper.append(icon);
    }
};

// نمایش datepicker شمسی
jalali_calendar.show_persian_datepicker = function(control) {
    if (typeof $.fn.persianDatepicker !== 'undefined') {
        control.$input.persianDatepicker({
            months: jalali_calendar.config.months,
            dowTitle: jalali_calendar.config.weekDays,
            shortDowTitle: jalali_calendar.config.shortWeekDays,
            persianNumbers: true,
            formatDate: "YYYY/MM/DD",
            onSelect: function() {
                const selected_date = control.$input.val();
                // تبدیل به میلادی و ذخیره
                frappe.call({
                    method: 'jalali_calendar.jalali_calendar.api.convert_to_gregorian',
                    args: {
                        jalali_date_str: selected_date
                    },
                    callback: function(r) {
                        if (r.message) {
                            control.$input.attr('data-gregorian', r.message);
                            control.$input.trigger('change');
                        }
                    }
                });
            }
        });
    } else {
        // Fallback to simple date input
        jalali_calendar.show_simple_datepicker(control);
    }
};

// Datepicker ساده
jalali_calendar.show_simple_datepicker = function(control) {
    const d = new frappe.ui.Dialog({
        title: 'انتخاب تاریخ شمسی',
        fields: [
            {
                label: 'سال',
                fieldname: 'year',
                fieldtype: 'Int',
                default: 1403
            },
            {
                label: 'ماه',
                fieldname: 'month',
                fieldtype: 'Select',
                options: jalali_calendar.config.months.map((m, i) => `${i+1} - ${m}`).join('\n')
            },
            {
                label: 'روز',
                fieldname: 'day',
                fieldtype: 'Int',
                default: 1
            }
        ],
        primary_action_label: 'تایید',
        primary_action(values) {
            const month_num = parseInt(values.month.split(' - ')[0]);
            const jalali_date = `${values.year}/${month_num}/${values.day}`;
            control.$input.val(jalali_date);
            
            // تبدیل به میلادی
            frappe.call({
                method: 'jalali_calendar.jalali_calendar.api.convert_to_gregorian',
                args: { jalali_date_str: jalali_date },
                callback: function(r) {
                    if (r.message) {
                        control.$input.attr('data-gregorian', r.message);
                        control.$input.trigger('change');
                    }
                }
            });
            
            d.hide();
        }
    });
    
    d.show();
};

// تبدیل و نمایش تاریخ
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
                control.$input.attr('title', `میلادی: ${control.value}`);
            }
        }
    });
};

// تبدیل همزمان به میلادی
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

// تبدیل همزمان به شمسی
jalali_calendar.sync_convert_to_jalali = function(gregorian_date) {
    let jalali = null;
    
    frappe.call({
        method: 'jalali_calendar.jalali_calendar.api.convert_to_jalali',
        args: { gregorian_date: gregorian_date },
        async: false,
        callback: function(r) {
            if (r.message && r.message.date) {
                jalali = r.message.date;
            }
        }
    });
    
    return jalali;
};

// =============== EVENT LISTENERS ===============

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
                frm.doc[field.fieldname] = gregorian_value;
            } else if (jalali_value && jalali_value.includes('/')) {
                const gregorian = jalali_calendar.sync_convert_to_gregorian(jalali_value);
                frm.doc[field.fieldname] = gregorian;
            }
        }
    });
};

// =============== INITIALIZATION ===============

// شروع اتوماتیک بعد از لود صفحه
$(document).ready(function() {
    jalali_calendar.check_user_preference();
});

// Export for global access
window.jalali_calendar = jalali_calendar;
