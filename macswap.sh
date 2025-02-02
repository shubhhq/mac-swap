#!/bin/bash

# Check for mode parameter
MODE=${2:-"file"}  # Default to file mode if not specified

echo "Detecting connected peripherals..."
KEYBOARD=$(blueutil --paired | grep -i keyboard | head -n 1 | awk '{print $2}')
POINTER=$(blueutil --paired | grep -iE 'mouse|trackpad' | head -n 1 | awk '{print $2}')

# Check if devices were found
if [ -z "$KEYBOARD" ]; then
    echo "No keyboard detected!"
    exit 1
fi

if [ -z "$POINTER" ]; then
    echo "No mouse or trackpad detected!"
    exit 1
fi

echo "Found keyboard: $KEYBOARD"
echo "Found pointing device: $POINTER"

# Disconnect peripherals from the current Mac
echo "Disconnecting peripherals..."
echo "Raw KEYBOARD MAC: $KEYBOARD"
echo "Raw POINTER MAC: $POINTER"
KEYBOARD_FORMATTED=$(echo $KEYBOARD | tr -d ',' | tr '-' ':')
POINTER_FORMATTED=$(echo $POINTER | tr -d ',' | tr '-' ':')
echo "Formatted KEYBOARD MAC: $KEYBOARD_FORMATTED"
echo "Formatted POINTER MAC: $POINTER_FORMATTED"
# blueutil --disconnect "$KEYBOARD_FORMATTED"
# blueutil --disconnect "$POINTER_FORMATTED"

# Wait for a few seconds to ensure disconnection
# sleep 5

# case "$MODE" in
#     "mail")
#         echo "Using email mode..."
#         osascript <<EOF
# tell application "Mail"
#     set newMessage to make new outgoing message with properties {subject:"Connect Peripherals", content:"Please connect the following peripherals:\n\nKeyboard: " & "$KEYBOARD_FORMATTED" & "\nPointing Device: " & "$POINTER_FORMATTED", visible:false}
#     tell newMessage
#         make new to recipient at end of to recipients with properties {address:"$1"}
#     end tell
#     send newMessage
#     delay 1
#     quit
# end tell
# EOF
#         ;;
#     "file")
#         echo "Using shared file mode..."
#         SHARED_FILE="/Users/Shared/peripherals_connect.txt"
#         echo "Writing peripheral information to shared file..."
#         echo "KEYBOARD=$KEYBOARD_FORMATTED" > "$SHARED_FILE"
#         echo "POINTER=$POINTER_FORMATTED" >> "$SHARED_FILE"
#         echo "TIMESTAMP=$(date +%s)" >> "$SHARED_FILE"
#         ;;
#     *)
#         echo "Invalid mode specified. Use 'mail' or 'file'"
#         exit 1
#         ;;
# esac

echo "Switching complete! Used $MODE mode."