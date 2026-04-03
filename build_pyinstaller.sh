#!/bin/bash

# Build script using PyInstaller (better Python 3.13 support)

set -e  # Exit on error

echo "======================================"
echo "Video Subtitle Translator - PyInstaller Build"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install pyinstaller

# Install other dependencies
pip install PySide6 deepl openai-whisper pysrt ffmpeg-python

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist *.spec

# Create the application with PyInstaller
echo "Building application with PyInstaller..."
pyinstaller --name="Video Subtitle Translator" \
    --windowed \
    --osx-bundle-identifier=com.translator.videosubtitles \
    --add-data="app:app" \
    --hidden-import=whisper \
    --hidden-import=deepl \
    --hidden-import=pysrt \
    --hidden-import=ffmpeg \
    --hidden-import=PySide6 \
    --hidden-import=torch \
    --collect-all whisper \
    --collect-all torch \
    --collect-all PySide6 \
    main.py

# Check if build succeeded
if [ -d "dist/Video Subtitle Translator.app" ]; then
    echo ""
    echo "======================================"
    echo "Build successful!"
    echo "======================================"
    echo ""
    echo "Application created at:"
    echo "  dist/Video Subtitle Translator.app"
    echo ""
    echo "To test the application:"
    echo "  open dist/"
    echo ""
    echo "To install to Applications folder:"
    echo "  cp -r \"dist/Video Subtitle Translator.app\" /Applications/"
    echo ""
    echo "Note: Make sure ffmpeg is installed:"
    echo "  brew install ffmpeg"
    echo ""
else
    echo "Build failed! Check the error messages above."
    exit 1
fi
