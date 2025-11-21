#!/bin/bash
set -e

pytest tests/webui/openbmc_auth_tests.py \
    --html=webui_report.html \
    --self-contained-html \
    -v