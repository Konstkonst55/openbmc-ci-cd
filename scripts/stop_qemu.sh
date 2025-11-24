#!/bin/bash

PID_FILE="/tmp/qemu.pid"

if [ -f "$PID_FILE" ]; then
    QEMU_PID=$(cat "$PID_FILE")
    echo "Found QEMU PID: $QEMU_PID"
    
    if ps -p "$QEMU_PID" > /dev/null 2>&1; then
        echo "Terminating QEMU process..."
        kill -TERM "$QEMU_PID"
        sleep 5
        
        if ps -p "$QEMU_PID" > /dev/null 2>&1; then
            echo "Force killing QEMU process..."
            kill -KILL "$QEMU_PID"
        fi
        
        echo "QEMU stopped successfully"
    else
        echo "QEMU process not found"
    fi
    
    rm -f "$PID_FILE"
else
    echo "PID file not found, searching for QEMU processes..."
    pkill -f "qemu-system-arm" || echo "No QEMU processes found"
fi