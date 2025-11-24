#!/bin/bash

cd /var/jenkins_home/workspace/tests

source /opt/venv/bin/activate
pip install -r requirements.txt

cd webui

pytest openbmc_auth_tests.py \
    --html=../artifacts/webui_tests/report.html \
    --self-contained-html \
    --junitxml=../artifacts/webui_tests/junit.xml \
    -v