#!/bin/bash

#echo off

ps -ah | grep bot.py -m 1 | awk '{print $1}' | xargs kill -1

sh env/bin/activate

screen python bot.py&

