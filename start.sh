#!/bin/bash
# Start script for Render.com
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 60
