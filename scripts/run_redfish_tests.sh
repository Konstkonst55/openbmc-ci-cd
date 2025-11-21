#!/bin/bash
cd tests/redfish
pytest test_redfish.py --bmc-url=https://localhost:2443 --username=root --password=0penBmc \
--html=../../test_report_redfish.html --self-contained-html --disable-warnings -v
