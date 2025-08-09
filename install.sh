#!/bin/bash

# Jalali Calendar App Installation Script
# نصب Custom App تقویم شمسی برای ERPNext

echo "========================================="
echo "Jalali Calendar App Installation"
echo "========================================="

# بررسی وجود bench
if ! command -v bench &> /dev/null; then
    echo "Error: Bench is not installed. Please install Frappe Bench first."
    exit 1
fi

# نام سایت را از کاربر بگیرید
read -p "Enter your ERPNext site name: " SITE_NAME

if [ -z "$SITE_NAME" ]; then
    echo "Error: Site name cannot be empty."
    exit 1
fi

echo "Installing Jalali Calendar App..."

# دانلود dependencies
echo "Installing Python dependencies..."
pip install persiantools jdatetime

# کپی app به apps directory
BENCH_PATH=$(pwd)
APP_PATH="$BENCH_PATH/apps/jalali_calendar"

if [ -d "$APP_PATH" ]; then
    echo "Warning: App already exists at $APP_PATH"
    read -p "Do you want to overwrite? (y/n): " OVERWRITE
    if [ "$OVERWRITE" != "y" ]; then
        echo "Installation cancelled."
        exit 0
    fi
    rm -rf "$APP_PATH"
fi

# کپی فایل‌ها
echo "Copying app files..."
cp -r jalali_calendar "$BENCH_PATH/apps/"

# نصب app
echo "Installing app to site..."
bench --site "$SITE_NAME" install-app jalali_calendar

# Clear cache
echo "Clearing cache..."
bench --site "$SITE_NAME" clear-cache

# Migrate
echo "Running migrations..."
bench --site "$SITE_NAME" migrate

# دانلود JavaScript libraries
echo "Downloading JavaScript libraries..."

# دانلود moment-jalaali
MOMENT_JALAALI_URL="https://unpkg.com/moment-jalaali@latest/build/moment-jalaali.js"
wget -O "$APP_PATH/public/js/moment-jalaali.min.js" "$MOMENT_JALAALI_URL"

# دانلود persianDatepicker
echo "Please manually download persianDatepicker from:"
echo "https://github.com/behzadi/persianDatepicker"
echo "And place the files in:"
echo "- $APP_PATH/public/js/persianDatepicker.min.js"
echo "- $APP_PATH/public/css/persianDatepicker.css"

# Build assets
echo "Building assets..."
bench build --app jalali_calendar

# Restart
echo "Restarting bench..."
bench restart

echo "========================================="
echo "Installation Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Download Persian Datepicker files manually"
echo "2. Go to User Settings and enable 'Use Jalali Calendar'"
echo "3. Refresh your browser"
echo ""
echo "For system-wide activation:"
echo "Go to System Settings and enable 'Use Jalali Calendar'"
