#!/bin/bash
#/home/qfpay/python/bin/python server.py debug $1
export PYTHONPATH=$PYTHONPATH:/home/zhaowei/github
watchmedo auto-restart -d . -p "*.py" python server.py debug $1
