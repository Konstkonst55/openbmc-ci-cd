#!/bin/bash
echo "Running WebUI tests..."

. venv/bin/activate

mkdir -p reports

cd tests/webui
pytest openbmc_auth_tests.py \
    -v \
    --html=../../reports/webui_test_report.html \
    --self-contained-html \
    --disable-warnings

cd ../..
echo "WebUI tests completed"