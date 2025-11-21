#!/bin/bash
echo "Running Redfish API tests..."

. venv/bin/activate

cd tests/redfish
python run_tests.py

pytest test_redfish.py \
    --bmc-url=${BMC_URL} \
    --username=${BMC_USERNAME} \
    --password=${BMC_PASSWORD} \
    -v \
    --html=../../redfish_test_report.html \
    --self-contained-html \
    --disable-warnings

cd ../..
echo "Redfish tests completed"