#!/bin/bash

cd /var/jenkins_home/workspace/tests

pip3 install -r requirements.txt

cd redfish

pytest test_redfish.py \
    --html=../artifacts/redfish_tests/report.html \
    --self-contained-html \
    --junitxml=../artifacts/redfish_tests/junit.xml \
    -v