#!/usr/bin/env bash


set -e

export PYTHONUNBUFFERED=1

cd /src

if [ ${PROJECT_RUNTIME_MODE} = "test" ]; then
    exec python -m pytest
else
    exec python run_scheduler.py
fi
