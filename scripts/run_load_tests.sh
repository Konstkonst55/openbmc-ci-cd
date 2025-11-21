#!/bin/bash
set -e

locust -f tests/load/locustfile.py \
    --headless \
    --users 20 \
    --spawn-rate 5 \
    --run-time 2m \
    --html=locust_report.html \
    --host=https://localhost:2443