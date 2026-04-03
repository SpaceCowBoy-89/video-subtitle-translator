#!/usr/bin/osascript

-- Simple launcher for Video Subtitle Translator
-- To use: Open in Script Editor and export as Application

-- Get the directory where this script is located
tell application "Finder"
    set scriptPath to POSIX path of (container of (path to me) as text)
end tell

-- Activate Python virtual environment and run the application
do shell script "cd " & quoted form of scriptPath & " && source venv/bin/activate && python main.py > /dev/null 2>&1 &"

-- Optional: Show a notification
display notification "Video Subtitle Translator is starting..." with title "Translator"
