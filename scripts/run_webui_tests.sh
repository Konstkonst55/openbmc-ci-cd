#!/bin/bash

cd /var/jenkins_home/workspace/tests

export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 2>/dev/null &
XVFB_PID=$!

sleep 2

cd webui

pytest openbmc_auth_tests.py \
    --html=../artifacts/webui_tests/report.html \
    --self-contained-html \
    --junitxml=../artifacts/webui_tests/junit.xml \
    -v

RESULT=$?

kill $XVFB_PID 2>/dev/null || true

exit $RESULT