#!/bin/sh

gunicorn -c .config/gunicorn.py -b "0.0.0.0:8000" server:app
