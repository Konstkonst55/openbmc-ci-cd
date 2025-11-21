#!/bin/bash

set -e

mkdir -p romulus
cd romulus

if ! command -v unzip >/dev/null 2>&1; then
    apt-get update
    apt-get install -y unzip
fi

wget -q https://jenkins.openbmc.org/job/ci-openbmc/lastSuccessfulBuild/distro=ubuntu,label=docker-builder,target=romulus/artifact/openbmc/build/tmp/deploy/images/romulus/romulus.zip

unzip -o romulus.zip

MTD_FILE=$(ls obmc-phosphor-image-romulus-*.static.mtd | head -n 1)

cd ..

qemu-system-arm \
  -m 256 \
  -M romulus-bmc \
  -nographic \
  -drive file=romulus/$MTD_FILE,format=raw,if=mtd \
  -net nic \
  -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu \
  &
sleep 40
