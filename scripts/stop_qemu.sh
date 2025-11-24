#!/bin/bash

PID_FILE="/tmp/qemu.pid"

if [ -f "$PID_FILE" ]; then
    QEMU_PID=$(cat "$PID_FILE")
    kill -TERM "$QEMU_PID" 2>/dev/null || true
    sleep 5
    kill -KILL "$QEMU_PID" 2>/dev/null || true
    rm -f "$PID_FILE"
fi

pkill -f "qemu-system-arm" || true