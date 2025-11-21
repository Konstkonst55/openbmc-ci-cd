#!/bin/bash
set -e

mkdir -p romulus
cd romulus

IMAGE_URL="https://jenkins.openbmc.org/job/ci-openbmc/lastSuccessfulBuild/artifact/openbmc/build/tmp/deploy/images/romulus/obmc-phosphor-image-romulus.static.mtd"

if [ ! -f obmc-phosphor-image-romulus.static.mtd ]; then
    echo "Downloading fixed OpenBMC image..."
    wget -q $IMAGE_URL -O obmc-phosphor-image-romulus.static.mtd
fi

echo "Starting QEMU with OpenBMC..."

qemu-system-arm \
    -m 512 \
    -M romulus-bmc \
    -nographic \
    -drive file=obmc-phosphor-image-romulus.static.mtd,format=raw,if=mtd \
    -net nic \
    -net user,hostfwd=tcp::2222-:22,hostfwd=tcp::2443-:443,hostfwd=udp::2623-:623,hostname=qemu \
    -serial mon:stdio