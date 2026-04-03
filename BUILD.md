# Building a Standalone macOS Application

This guide explains how to create a standalone **Video Subtitle Translator.app** that can be launched by double-clicking, without needing to open Terminal.

## Prerequisites

1. **Python 3.8+** installed
2. **ffmpeg** installed and in PATH:
   ```bash
   brew install ffmpeg
   ```
3. **Xcode Command Line Tools** (if not already installed):
   ```bash
   xcode-select --install
   ```

## Method 1: Using py2app (Recommended for macOS)

### Step 1: Install Dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install all dependencies including py2app
pip install -r requirements.txt
```

### Step 2: Build the Application

```bash
# Clean previous builds
rm -rf build dist

# Build the .app bundle
python setup.py py2app
```

This creates `dist/Video Subtitle Translator.app`

### Step 3: Test the Application

```bash
# Run from command line first to test
./dist/Video\ Subtitle\ Translator.app/Contents/MacOS/Video\ Subtitle\ Translator

# Or double-click the app in Finder
open dist/
```

### Step 4: Move to Applications (Optional)

```bash
cp -r "dist/Video Subtitle Translator.app" /Applications/
```

### Troubleshooting py2app Build

If the build fails due to missing modules:
1. Check the error message for missing packages
2. Add them to the `packages` list in `setup.py`
3. Rebuild

## Method 2: Using PyInstaller (Alternative)

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Create Spec File

```bash
pyi-makespec --windowed --name="Video Subtitle Translator" main.py
```

### Step 3: Build

```bash
pyinstaller "Video Subtitle Translator.spec"
```

## Method 3: Simple Launch Script (Quick Solution)

If you just want a clickable icon without full packaging:

### Step 1: Create an AppleScript Application

1. Open **Script Editor** (in `/Applications/Utilities/`)
2. Paste this script:

```applescript
do shell script "cd ~/Translator && source venv/bin/activate && python main.py > /dev/null 2>&1 &"
```

3. Save as **Application** (File → Export → File Format: Application)
4. Save to Desktop or Applications folder

### Step 2: Add Custom Icon (Optional)

1. Find an icon image (512x512 PNG recommended)
2. Get Info on the .app (Cmd+I)
3. Drag icon to the small icon in top-left of Info window

## Important Notes

### ffmpeg Requirement

The built application **still requires ffmpeg** to be installed on the system. Users need to:
```bash
brew install ffmpeg
```

To bundle ffmpeg with the app (advanced):
1. Copy ffmpeg binary into the app bundle:
   ```bash
   cp $(which ffmpeg) "dist/Video Subtitle Translator.app/Contents/MacOS/"
   ```
2. Modify code to use bundled ffmpeg

### First Launch Issues

**Gatekeeper Warning**: When first launching, macOS may show "unidentified developer" warning:
1. Right-click the app → Open
2. Click "Open" in the dialog
3. Or: System Preferences → Security & Privacy → "Open Anyway"

To avoid this, sign the application:
```bash
codesign --deep --force --sign - "dist/Video Subtitle Translator.app"
```

### Large Application Size

The built application may be **large (1-3 GB)** because it includes:
- PySide6 (Qt framework)
- Whisper model files
- PyTorch dependencies

To reduce size:
- Use `--excludes` in setup.py for unnecessary packages
- Store Whisper models externally (downloaded on first use)

## Distribution

### For Personal Use
Just copy the .app to /Applications

### For Other Users
Create a DMG installer:
```bash
# Install create-dmg
brew install create-dmg

# Create DMG
create-dmg \
  --volname "Video Subtitle Translator" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --app-drop-link 450 200 \
  "VideoSubtitleTranslator.dmg" \
  "dist/Video Subtitle Translator.app"
```

Users can then:
1. Download the DMG
2. Drag the app to Applications folder
3. Install ffmpeg: `brew install ffmpeg`
4. Launch the app

## Automated Build Script

Use the included `build.sh` script:
```bash
chmod +x build.sh
./build.sh
```

This automates the entire build process.
