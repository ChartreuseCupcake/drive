#!/bin/bash
source /etc/bash_completion.d/virtualenvwrapper
workon ev3_py34
echo Started virtualenv
python btnwait.py
python testdrive.py
sleep 5
