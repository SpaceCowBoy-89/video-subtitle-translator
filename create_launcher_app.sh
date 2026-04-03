#!/bin/bash

# Quick script to create a simple clickable launcher application
# This is faster than building with py2app but less polished

echo "Creating launcher application..."

# Create AppleScript app bundle
mkdir -p "Translator.app/Contents/MacOS"
mkdir -p "Translator.app/Contents/Resources"

# Create Info.plist
cat > "Translator.app/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launcher</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>com.translator.videosubtitles</string>
    <key>CFBundleName</key>
    <string>Video Subtitle Translator</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
</dict>
</plist>
EOF

# Create launcher script
cat > "Translator.app/Contents/MacOS/launcher" << 'EOF'
#!/bin/bash

# Get the app bundle directory
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROJECT_DIR="$(dirname "$APP_DIR")"

# Launch the application
cd "$PROJECT_DIR"
if [ -d "venv" ]; then
    source venv/bin/activate
fi
python main.py &
EOF

chmod +x "Translator.app/Contents/MacOS/launcher"

echo ""
echo "✓ Launcher app created: Translator.app"
echo ""
echo "To use:"
echo "  1. Double-click Translator.app"
echo "  2. (Optional) Drag to Applications folder"
echo ""
echo "Note: This is a simple launcher. For a professional app bundle, use build.sh instead."
