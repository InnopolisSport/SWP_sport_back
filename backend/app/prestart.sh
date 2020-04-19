#! /usr/bin/env bash

# Let the DB start
python /app/app/backend_pre_start.py

# Copy statics to Nginx
cp /app/app/static / -r
