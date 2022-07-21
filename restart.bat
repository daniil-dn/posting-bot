#!/bin/bash


ps -au | grep bot.py -m 1 | awk '{print $2}' | xargs kill -2

source env/bin/activate

python bot.py&

