#!/bin/bash

# Download External Dependencies for Jalali Calendar
# دانلود وابستگی‌های خارجی و ذخیره لوکال

echo "========================================="
echo "📥 Downloading External Dependencies"
echo "========================================="

# Set paths
if [ -z "$1" ]; then
    APP_PATH="./jalali_calendar"
else
    APP_PATH="$1"
fi

JS_PATH="$APP_PATH/public/js"
CSS_PATH="$APP_PATH/public/css"
FONTS_PATH="$APP_PATH/public/fonts"

# Create directories if not exist
mkdir -p "$JS_PATH"
mkdir -p "$CSS_PATH"
mkdir -p "$FONTS_PATH"

echo "📁 Directories created/verified"

# Function to download with retry
download_with_retry() {
    local url=$1
    local output=$2
    local max_attempts=3
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        echo "  Attempt $attempt of $max_attempts..."
        if curl -L -f -o "$output" "$url" 2>/dev/null || wget -O "$output" "$url" 2>/dev/null; then
            echo "  ✅ Downloaded successfully"
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 2
    done
    
    echo "  ❌ Failed to download after $max_attempts attempts"
    return 1
}

# 1. Download Moment-Jalaali
echo ""
echo "1️⃣ Downloading Moment-Jalaali..."
MOMENT_URL="https://unpkg.com/moment-jalaali@0.10.0/build/moment-jalaali.js"
download_with_retry "$MOMENT_URL" "$JS_PATH/moment-jalaali.min.js"

# 2. Download Persian Datepicker JS
echo ""
echo "2️⃣ Downloading Persian Datepicker JS..."
DATEPICKER_JS_URL="https://raw.githubusercontent.com/behzadi/persianDatepicker/master/js/persianDatepicker.min.js"
download_with_retry "$DATEPICKER_JS_URL" "$JS_PATH/persianDatepicker.min.js"

# 3. Download Persian Datepicker CSS
echo ""
echo "3️⃣ Downloading Persian Datepicker CSS..."
DATEPICKER_CSS_URL="https://raw.githubusercontent.com/behzadi/persianDatepicker/master/css/persianDatepicker-default.css"
download_with_retry "$DATEPICKER_CSS_URL" "$CSS_PATH/persianDatepicker.css"

# 4. Download Vazir Font (Optional but recommended)
echo ""
echo "4️⃣ Downloading Vazir Font..."
echo "  Do you want to download Vazir font for better Persian display? (y/n)"
read -r DOWNLOAD_FONT

if [ "$DOWNLOAD_FONT" = "y" ]; then
    # Download Vazir font files
    VAZIR_BASE="https://github.com/rastikerdar/vazir-font/releases/download/v30.1.0"
    
    echo "  Downloading Vazir Regular..."
    download_with_retry "$VAZIR_BASE/vazir-font-v30.1.0.zip" "/tmp/vazir.zip"
    
    if [ -f "/tmp/vazir.zip" ]; then
        # Extract font files
        unzip -q "/tmp/vazir.zip" -d "/tmp/vazir_temp"
        
        # Copy web fonts
        cp /tmp/vazir_temp/fonts/webfonts/*.woff2 "$FONTS_PATH/" 2>/dev/null
        cp /tmp/vazir_temp/fonts/webfonts/*.woff "$FONTS_PATH/" 2>/dev/null
        
        # Clean up
        rm -rf "/tmp/vazir.zip" "/tmp/vazir_temp"
        
        echo "  ✅ Vazir font installed"
        
        # Add font-face to CSS
        cat >> "$CSS_PATH/jalali_calendar.css" << 'EOF'

/* Vazir Font */
@font-face {
    font-family: 'Vazir';
    src: url('../fonts/Vazir-Regular.woff2') format('woff2'),
         url('../fonts/Vazir-Regular.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}

@font-face {
    font-family: 'Vazir';
    src: url('../fonts/Vazir-Bold.woff2') format('woff2'),
         url('../fonts/Vazir-Bold.woff') format('woff');
    font-weight: bold;
    font-style: normal;
}

/* Apply Vazir to Jalali elements */
.jalali-date,
.jalali-calendar-widget,
.persianDatepicker {
    font-family: 'Vazir', Tahoma, Arial, sans-serif !important;
}
EOF
        echo "  ✅ Font-face CSS added"
    fi
fi

# 5. Create fallback files if downloads failed
echo ""
echo "5️⃣ Checking downloaded files..."

# Check moment-jalaali
if [ ! -f "$JS_PATH/moment-jalaali.min.js" ] || [ ! -s "$JS_PATH/moment-jalaali.min.js" ]; then
    echo "  ⚠️  moment-jalaali.min.js not found or empty"
    echo "  Creating placeholder with CDN fallback..."
    cat > "$JS_PATH/moment-jalaali.min.js" << 'EOF'
// Fallback: Load from CDN
(function() {
    console.warn('Loading moment-jalaali from CDN as local file is missing');
    var script = document.createElement('script');
    script.src = 'https://unpkg.com/moment-jalaali@latest/build/moment-jalaali.js';
    script.async = false;
    document.head.appendChild(script);
})();
EOF
fi

# Check persianDatepicker
if [ ! -f "$JS_PATH/persianDatepicker.min.js" ] || [ ! -s "$JS_PATH/persianDatepicker.min.js" ]; then
    echo "  ⚠️  persianDatepicker.min.js not found or empty"
    echo "  Creating placeholder with CDN fallback..."
    cat > "$JS_PATH/persianDatepicker.min.js" << 'EOF'
// Fallback: Load from CDN
(function() {
    console.warn('Loading persianDatepicker from CDN as local file is missing');
    var script = document.createElement('script');
    script.src = 'https://raw.githubusercontent.com/behzadi/persianDatepicker/master/js/persianDatepicker.min.js';
    script.async = false;
    document.head.appendChild(script);
})();
EOF
fi

# 6. Create integrity check file
echo ""
echo "6️⃣ Creating integrity check file..."
cat > "$APP_PATH/public/dependencies.json" << EOF
{
    "dependencies": {
        "moment-jalaali": {
            "version": "0.10.0",
            "local": "js/moment-jalaali.min.js",
            "cdn": "https://unpkg.com/moment-jalaali@0.10.0/build/moment-jalaali.js",
            "size": $(stat -f%z "$JS_PATH/moment-jalaali.min.js" 2>/dev/null || echo "0")
        },
        "persianDatepicker": {
            "version": "0.1.0",
            "local_js": "js/persianDatepicker.min.js",
            "local_css": "css/persianDatepicker.css",
            "cdn_js": "https://raw.githubusercontent.com/behzadi/persianDatepicker/master/js/persianDatepicker.min.js",
            "cdn_css": "https://raw.githubusercontent.com/behzadi/persianDatepicker/master/css/persianDatepicker-default.css"
        },
        "vazir-font": {
            "version": "30.1.0",
            "installed": $([ -f "$FONTS_PATH/Vazir-Regular.woff2" ] && echo "true" || echo "false")
        }
    },
    "downloaded_at": "$(date -u +"%Y-%m-%d %H:%M:%S UTC")"
}
EOF

echo ""
echo "========================================="
echo "📊 Download Summary:"
echo "========================================="

# Check what was successfully downloaded
echo ""
if [ -f "$JS_PATH/moment-jalaali.min.js" ] && [ -s "$JS_PATH/moment-jalaali.min.js" ]; then
    echo "✅ moment-jalaali.min.js - OK ($(du -h "$JS_PATH/moment-jalaali.min.js" | cut -f1))"
else
    echo "❌ moment-jalaali.min.js - Missing or empty"
fi

if [ -f "$JS_PATH/persianDatepicker.min.js" ] && [ -s "$JS_PATH/persianDatepicker.min.js" ]; then
    echo "✅ persianDatepicker.min.js - OK ($(du -h "$JS_PATH/persianDatepicker.min.js" | cut -f1))"
else
    echo "❌ persianDatepicker.min.js - Missing or empty"
fi

if [ -f "$CSS_PATH/persianDatepicker.css" ] && [ -s "$CSS_PATH/persianDatepicker.css" ]; then
    echo "✅ persianDatepicker.css - OK ($(du -h "$CSS_PATH/persianDatepicker.css" | cut -f1))"
else
    echo "❌ persianDatepicker.css - Missing or empty"
fi

if [ -f "$FONTS_PATH/Vazir-Regular.woff2" ]; then
    echo "✅ Vazir Font - Installed"
else
    echo "ℹ️  Vazir Font - Not installed (optional)"
fi

echo ""
echo "========================================="
echo "✨ Process completed!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Run: bench build --app jalali_calendar"
echo "2. Run: bench clear-cache"
echo "3. Restart: bench restart"
echo ""
echo "If any downloads failed, you can:"
echo "1. Re-run this script"
echo "2. Manually download from the URLs above"
echo "3. The app will fallback to CDN if needed"
