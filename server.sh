#!/bin/bash

source env/bin/activate
PYTHONPATH=src python src/id3img/server.py -l DEBUG /music/mp3 > ~/log/id3img.log 2>&1 &

