#!/bin/bash

# Enhanced Jalali Calendar App Installation Script
# نصب کامل و خودکار Custom App تقویم شمسی برای ERPNext

echo "========================================="
echo "🗓️ Jalali Calendar Enhanced Installation"
echo "========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}This script should not be run as root!${NC}"
   exit 1
fi

# Check for bench
if ! command -v bench &> /dev/null; then
    echo -e "${RED}Error: Bench is not installed. Please install Frappe Bench first.${NC}"
    exit 1
fi

# Get site name
read -p "Enter your ERPNext site name: " SITE_NAME

if [ -z "$SITE_NAME" ]; then
    echo -e "${RED}Error: Site name cannot be empty.${NC}"
    exit 1
fi

# Check if site exists
if ! bench --site "$SITE_NAME" list-apps &> /dev/null; then
    echo -e "${RED}Error: Site '$SITE_NAME' does not exist.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Site found: $SITE_NAME${NC}"

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install persiantools jdatetime --quiet

# Get bench path
BENCH_PATH=$(pwd)
APP_PATH="$BENCH_PATH/apps/jalali_calendar"

# Check if app already exists
if [ -d "$APP_PATH" ]; then
    echo -e "${YELLOW}Warning: App already exists at $APP_PATH${NC}"
    read -p "Do you want to reinstall? (y/n): " REINSTALL
    if [ "$REINSTALL" != "y" ]; then
        echo "Installation cancelled."
        exit 0
    fi
    
    # Uninstall existing app
    echo -e "${YELLOW}Uninstalling existing app...${NC}"
    bench --site "$SITE_NAME" uninstall-app jalali_calendar --yes 2>/dev/null || true
    rm -rf "$APP_PATH"
fi

# Copy app files
echo -e "${YELLOW}Copying app files...${NC}"
cp -r jalali_calendar "$BENCH_PATH/apps/"

# Download JavaScript libraries
echo -e "${YELLOW}Downloading JavaScript libraries...${NC}"

# Download moment-jalaali
echo "  Downloading moment-jalaali..."
curl -s -o "$APP_PATH/public/js/moment-jalaali.min.js" \
     "https://unpkg.com/moment-jalaali@latest/build/moment-jalaali.js"

# Download Persian Datepicker
echo "  Downloading Persian Datepicker..."
DATEPICKER_URL="https://raw.githubusercontent.com/behzadi/persianDatepicker/master"
curl -s -o "$APP_PATH/public/js/persianDatepicker.min.js" \
     "$DATEPICKER_URL/js/persianDatepicker.min.js"
curl -s -o "$APP_PATH/public/css/persianDatepicker.css" \
     "$DATEPICKER_URL/css/persianDatepicker-default.css"

echo -e "${GREEN}✓ JavaScript libraries downloaded${NC}"

# Install app
echo -e "${YELLOW}Installing app to site...${NC}"
bench --site "$SITE_NAME" install-app jalali_calendar

# Run migrations
echo -e "${YELLOW}Running migrations...${NC}"
bench --site "$SITE_NAME" migrate

# Build assets
echo -e "${YELLOW}Building assets...${NC}"
bench build --app jalali_calendar

# Clear cache
echo -e "${YELLOW}Clearing cache...${NC}"
bench --site "$SITE_NAME" clear-cache

# Set default configuration
echo -e "${YELLOW}Setting up default configuration...${NC}"
bench --site "$SITE_NAME" execute jalali_calendar.jalali_calendar.install.after_install

# Restart services
echo -e "${YELLOW}Restarting services...${NC}"
bench restart

echo ""
echo "========================================="
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo "========================================="
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Login to ERPNext"
echo "2. Go to: Settings > Jalali Calendar Settings"
echo "3. Enable 'فعال' (Enabled) checkbox"
echo "4. Configure your preferences"
echo "5. For individual users: User > Edit > 'استفاده از تقویم شمسی'"
echo ""
echo "⌨️ Keyboard shortcuts:"
echo "  • Ctrl+Shift+T : Show today in Jalali"
echo "  • Ctrl+Shift+J : Toggle Jalali calendar"
echo "  • Ctrl+Shift+C : Show month calendar"
echo ""
echo -e "${GREEN}Enjoy your Jalali Calendar! 🎉${NC}"
