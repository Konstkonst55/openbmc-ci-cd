#!/bin/bash

set -e

cd /var/jenkins_home/workspace/romulus

QEMU_LOG="/tmp/qemu.log"

qemu-system-arm \
    -m 256 \
    -M romulus-bmc \
    -nographic \
    -drive file=obmc-phosphor-image-romulus-20251003025918.static.mtd,format=raw,if=mtd \
    -net nic \
    -net user,hostfwd=tcp::2443-:443,hostfwd=tcp::2222-:22,hostfwd=udp::2623-:623 \
    > "$QEMU_LOG" 2>&1 &

QEMU_PID=$!
echo "$QEMU_PID" > /tmp/qemu.pid

timeout 60 bash -c 'until curl -k -s https://localhost:2443 > /dev/null; do sleep 5; done'