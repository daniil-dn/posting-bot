#!/bin/bash

#echo off

source env/bin/activate

ps -ah | grep bot.py -m 1 | awk '{print $1}' | kill -1

python bot.py

