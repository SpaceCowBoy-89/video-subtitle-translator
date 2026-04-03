#!/bin/bash

echo "Pushing to GitHub..."
echo ""
echo "If this fails, you may need to:"
echo "1. Create the repository on GitHub first: https://github.com/new"
echo "2. Authenticate with GitHub (it will prompt you)"
echo ""

git push -u origin main

echo ""
echo "✅ Done! Your code is now on GitHub:"
echo "   https://github.com/SpaceCowBoy-89/video-subtitle-translator"
echo ""
echo "To free up space on your laptop, you can now run:"
echo "   ./cleanup.sh"
