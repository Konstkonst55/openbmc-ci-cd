#!/bin/bash

cd /var/jenkins_home/workspace/tests

source /opt/venv/bin/activate
pip install -r requirements.txt

cd redfish

pytest test_redfish.py \
    --html=../artifacts/redfish_tests/report.html \
    --self-contained-html \
    --junitxml=../artifacts/redfish_tests/junit.xml \
    -v