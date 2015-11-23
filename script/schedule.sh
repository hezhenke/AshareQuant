#!/bin/bash

BASE_DIR=`dirname $0`/../

export PATH
export PYTHONPATH=$BASE_DIR:$PYTHONPATH

dirname $0 
echo $PYTHONPATH
/usr/bin/python /home/jacob/pystock/AshareQuant/script/schedule.py
