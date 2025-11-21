#!/bin/bash
echo "Starting QEMU with OpenBMC..."

qemu-system-arm -m 256 \
    -M romulus-bmc \
    -nographic \
    -drive file=${QEMU_IMAGE:-romulus/obmc-phosphor-image-romulus-20251003025918.static.mtd},format=raw,if=mtd \
    -net nic \
    -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu \
    &
    
QEMU_PID=$!
echo $QEMU_PID > /tmp/qemu_pid.txt
echo "QEMU started with PID: $QEMU_PID"