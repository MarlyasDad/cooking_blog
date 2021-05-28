#!/usr/bin/env bash

echo "Running migrations"
python3.9 test_data.py

exec "$@"
