#!/bin/bash

cd /var/jenkins_home/workspace/tests

pip3 install -r requirements.txt

cd load

locust -f locustfile.py \
    --host=https://localhost:2443 \
    --users=5 \
    --spawn-rate=1 \
    --run-time=30s \
    --headless \
    --html=../artifacts/load_tests/locust_report.html \
    --csv=../artifacts/load_tests/locust_stats