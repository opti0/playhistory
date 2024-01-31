#!/bin/bash

#to be run as root in debian OS

#exit on error
set -e

#install python3 and its module manager.
apt install python3 python3-pip -y
#using pip3 install virtual enviroment
pip3 install virtualenv

#make virtualenviroment with python3 interpreter
virtualenv app/venv -p $(which python3)

#install requirements
app/venv/bin/pip3 install -r requirements.txt

# make database
app/venv/bin/python3 app/db.py create

echo 'Install script finished successfully!'
