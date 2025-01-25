#!/bin/bash


connect_devices() {
    local keyboard=$1
    local pointer=$2
    
    echo "Attempting to connect to peripherals..."
    echo "Keyboard: $keyboard"
    echo "Pointing device: $pointer"
    
    blueutil --connect "$keyboard"
    sleep 2
    blueutil --connect "$pointer"
    
    echo "Connection attempts completed"
}

# Function to check Mail for new messages. Maybe I am going to use a shared file or gmail API to make this faster.
check_mail() {
    osascript <<EOF
    tell application "Mail"
        set currentTime to (current date)
        set oneMinuteAgo to currentTime - 60 -- 60 seconds = 1 minute
        set newMessages to messages of inbox whose subject is "Connect Peripherals" and read status is false and date received > oneMinuteAgo
        if (count of newMessages) > 0 then
            set latestMessage to item 1 of newMessages
            set messageContent to content of latestMessage
            set read status of latestMessage to true
            return messageContent
        end if
        return ""
    end tell
EOF
}

echo "Starting peripheral connection monitor..."
echo "Waiting for connection request email..."

# Main loop
# this is inefficient, but it works, make it better later
# @shubh add device identification so the target and source can be differentiated
while true; do
    # Check for new emails
    MESSAGE_CONTENT=$(check_mail)
    
    if [ ! -z "$MESSAGE_CONTENT" ]; then
        echo "Received connection request!"
        
        # Extract MAC addresses from the email content
        KEYBOARD_MAC=$(echo "$MESSAGE_CONTENT" | grep "Keyboard:" | cut -d' ' -f2)
        POINTER_MAC=$(echo "$MESSAGE_CONTENT" | grep "Pointing Device:" | cut -d' ' -f3)
        
        if [ ! -z "$KEYBOARD_MAC" ] && [ ! -z "$POINTER_MAC" ]; then
            connect_devices "$KEYBOARD_MAC" "$POINTER_MAC"
        else
            echo "Failed to parse device addresses from email"
        fi
    fi
    
    sleep 5
done 