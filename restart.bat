#!/bin/bash

#echo off

sh env/bin/activate

ps -ah | grep bot.py -m 1 | awk '{print $1}' | xargs kill -1

screen python bot.py

