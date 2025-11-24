#!/bin/bash
set -e

cd romulus

MTD_FILE=$(find . -name "*.static.mtd" | head -1)

if [ -z "$MTD_FILE" ]; then
    echo "mtd файл не найден!"
    exit 1
fi

echo "mtd файл найден: $MTD_FILE"

QEMU_LOG="/tmp/qemu.log"

nohup qemu-system-arm \
    -m 256 \
    -M romulus-bmc \
    -nographic \
    -drive file="$MTD_FILE",format=raw,if=mtd \
    -net nic \
    -net user,hostfwd=tcp::2222-:22,hostfwd=tcp::2443-:443,hostfwd=udp::2623-:623,hostname=qemu \
    > "$QEMU_LOG" 2>&1 &

QEMU_PID=$!
echo "QEMU запущен с PID: $QEMU_PID"

echo "$QEMU_PID" > /tmp/qemu.pid

echo "Ожидание запуска OpenBMC..."
MAX_WAIT=120
WAIT_TIME=0
INTERVAL=10

while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    if curl -k -s https://localhost:2443 > /dev/null 2>&1; then
        echo "OpenBMC успешно запущен и доступен на https://localhost:2443"
        echo "QEMU PID: $QEMU_PID"
        exit 0
    fi
    
    echo "Ожидание... ($WAIT_TIME/$MAX_WAIT секунд)"
    sleep $INTERVAL
    WAIT_TIME=$((WAIT_TIME + INTERVAL))
done

echo "OpenBMC не запустился в течение $MAX_WAIT секунд"
echo "Логи QEMU:"
tail -50 "$QEMU_LOG"
exit 1