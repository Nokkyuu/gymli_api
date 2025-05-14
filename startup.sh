#!/bin/bash
export PYTHONUNBUFFERED=1
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app