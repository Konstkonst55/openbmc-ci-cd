#!/bin/bash
set -e

pytest tests/redfish/test_redfish.py \
    --bmc-url=https://localhost:2443 \
    --username=root \
    --password=0penBmc \
    -v \
    --html=redfish_report.html \
    --self-contained-html \
    --disable-warnings