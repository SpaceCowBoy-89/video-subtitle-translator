#!/bin/bash

# Build script for Video Subtitle Translator macOS application

set -e  # Exit on error

echo "======================================"
echo "Video Subtitle Translator - Build Script"
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
pip install -r requirements.txt

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Build the application
echo "Building application bundle with py2app..."
python setup.py py2app

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
