#!/bin/bash

gunicorn -c ../conf/gunicorn_setting.py server:app
