#!/bin/bash
cd tests/load
locust -f locustfile.py --headless -u 10 -r 2 -t 30s --csv ../../locust
mv ../../locust_stats_requests.csv ../../locust_stats.csv
