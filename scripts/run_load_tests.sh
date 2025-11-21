#!/bin/bash
echo "Running load tests with Locust..."

. venv/bin/activate

cd tests/load
locust -f locustfile.py \
    --headless \
    --users 2 \
    --spawn-rate 1 \
    --run-time 1m \
    --html=../../locust_report.html \
    --host=${BMC_URL}

cd ../..
echo "Load tests completed"