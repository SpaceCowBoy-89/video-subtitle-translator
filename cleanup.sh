#!/bin/bash

echo "======================================"
echo "Cleanup Script - Free Up Disk Space"
echo "======================================"
echo ""
echo "This will delete:"
echo "  - venv/ (1.9GB)"
echo "  - dist/ (2.3GB)"
echo "  - build/ (142MB)"
echo ""
echo "Total space freed: ~4.3GB"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing build artifacts..."
    rm -rf venv/ build/ dist/ "Video Subtitle Translator.spec" __pycache__ app/__pycache__ app/*/__pycache__
    echo ""
    echo "✅ Cleanup complete! Freed ~4.3GB"
    echo ""
    echo "To rebuild the app later:"
    echo "  ./build_pyinstaller.sh"
    echo ""
    echo "The app is already installed in /Applications/"
else
    echo "Cleanup cancelled."
fi
