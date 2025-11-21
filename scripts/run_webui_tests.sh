#!/bin/bash
cd tests/webui
pytest openbmc_auth_tests.py --html=../../webui_report.html --self-contained-html -v
