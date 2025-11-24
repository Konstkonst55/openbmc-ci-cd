#!/bin/bash
set -e

cd tests

locust -f load/locustfile.py \
    --headless \
    --users 5 \
    --spawn-rate 1 \
    --run-time 1m \
    --html=locust_report.html \
    --host=https://localhost:2443