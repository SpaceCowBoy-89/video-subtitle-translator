# Quick Start Guide - Standalone Application

This guide helps you create a **double-clickable application** that doesn't require using Terminal.

## Prerequisites

First, ensure you have these installed:

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install ffmpeg
brew install ffmpeg

# Install Python 3 (if not installed)
brew install python@3.11
```

## Option 1: Quick Launcher (Fastest - 30 seconds)

This creates a simple clickable app that launches the Python script:

```bash
cd /Users/patrickappo/Translator

# Install dependencies first
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create launcher app
./create_launcher_app.sh
```

Now you can double-click `Translator.app` to launch!

**Pros**: Very fast, small size
**Cons**: Less polished, shows Terminal briefly when launching

---

## Option 2: Full Application Bundle (Recommended - 5 minutes)

This creates a professional macOS application with all dependencies bundled:

```bash
cd /Users/patrickappo/Translator

# Run automated build script
./build.sh
```

The application will be created at: `dist/Video Subtitle Translator.app`

**To install to Applications folder:**
```bash
cp -r "dist/Video Subtitle Translator.app" /Applications/
```

**Pros**: Professional, no Terminal window, self-contained
**Cons**: Larger file size (~1-2 GB), longer build time

---

## First Launch

When you first open the app, macOS may show a security warning:

1. **Right-click** the app → **Open**
2. Click **"Open"** in the dialog

Or go to: **System Preferences → Security & Privacy → "Open Anyway"**

---

## Setting Up the Application

1. **Launch the app** (double-click)
2. Go to **Settings → Preferences**
3. Enter your **DeepL API key** (get one at https://www.deepl.com/pro-api)
4. Choose **Whisper model size** (start with "base")
5. Click **OK**

---

## Using the Application

1. **Select languages**: Source (or Auto-Detect) and Target
2. **Add files**: Click "Add Files..." or drag & drop videos/subtitles
3. **Choose options**:
   - Subtitle source: Auto (recommended), Whisper, or Embedded
   - Output format: SRT or VTT
   - ✓ Burn subtitles into video (optional)
4. **Click Start**
5. **Wait** for processing to complete

Output files appear in the same folder as input files (or your chosen output directory).

---

## Troubleshooting

### "Application can't be opened"
- Right-click → Open (first time only)
- Or: System Preferences → Security & Privacy → Open Anyway

### "ffmpeg not found"
```bash
brew install ffmpeg
```

### "DeepL API Error"
- Check your API key in Settings
- Verify you have available characters in your DeepL account

### App crashes on launch
```bash
# Test from terminal to see errors:
cd /Users/patrickappo/Translator
source venv/bin/activate
python main.py
```

### Build failed
```bash
# Clean and retry:
rm -rf build dist venv
./build.sh
```

---

## Updating the Application

If you make code changes and want to rebuild:

```bash
cd /Users/patrickappo/Translator

# For quick launcher:
./create_launcher_app.sh

# For full application:
./build.sh
```

---

## Removing the Application

```bash
# Remove installed app
rm -rf "/Applications/Video Subtitle Translator.app"

# Or remove quick launcher
rm -rf "/Applications/Translator.app"

# Remove project folder (if desired)
rm -rf /Users/patrickappo/Translator
```

---

## Next Steps

- Read the full [README.md](README.md) for detailed features
- Check [BUILD.md](BUILD.md) for advanced build options
- Run tests: `python -m pytest tests/ -v`

Enjoy translating! 🎬🌍
