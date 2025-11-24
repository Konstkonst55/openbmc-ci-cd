#!/bin/bash
set -e

cd tests

pytest webui/openbmc_auth_tests.py \
    --html=webui_report.html \
    --self-contained-html \
    -v