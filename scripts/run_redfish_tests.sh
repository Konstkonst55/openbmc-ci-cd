#!/bin/bash
echo "Running Redfish API tests..."

if [ -f "venv/bin/activate" ]; then
    . venv/bin/activate
else
    echo "Virtual environment not found, using system Python"
fi

mkdir -p reports

cd tests/redfish

python run_tests.py || {
    pytest test_simple.py -v --html=../../reports/redfish_test_report.html --self-contained-html
}

cd ../..
echo "Redfish tests completed"