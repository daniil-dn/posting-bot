#!/bin/bash

#echo off

ps -ah | grep bot.py -m 1 | awk '{print $1}' | xargs kill -1

source env/bin/activate

python bot.py&

