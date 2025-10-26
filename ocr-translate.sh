#!/bin/bash

# Define a temporary file path.
# Using $$ makes the filename unique to this specific script execution.
TMP_FILE="/tmp/screenshot-ocr-$$.png"

# 1. Use gnome-screenshot to select an area (-a) and save it to our temp file (-f).
# If you cancel the selection, the command will fail and the script will exit.
gnome-screenshot -a -f "$TMP_FILE"
if [ ! -f "$TMP_FILE" ]; then
    exit 1
fi

# 2. Feed the saved screenshot file to Tesseract.
# It reads the file, performs OCR with Japanese language pack (-l jpn), and prints to stdout.
#
# 3. Pipe the Japanese text to translate-shell to get the brief English translation.

#ORIGINAL_TEXT=$(cat $TMP_FILE)
ORIGINAL_TEXT=$(tesseract "$TMP_FILE" stdout -l jpn)

# 2. Pass the original text variable to the translator
TRANSLATED_TEXT=$(echo "$ORIGINAL_TEXT" | trans --brief :en)
# For using with LFM API:
# TRANSLATED_TEXT=$(tesseract "$TMP_FILE" stdout -l jpn | cli_translate.py)

# 4. Clean up the temporary screenshot file immediately.
rm "$TMP_FILE"

# 5. Copy the result to the clipboard and display it in a dialog box.
if [ -n "$TRANSLATED_TEXT" ]; then
    echo "$TRANSLATED_TEXT" | wl-copy
    zenity --info --title="OCR-translate" --text="$ORIGINAL_TEXT:\n$TRANSLATED_TEXT" --no-wrap
else
    zenity --error --title="Error" --text="Could not extract or translate text."
fi
