#!/usr/bin/env bash

python3 -m piper \
  --model en_US-lessac-medium \
  --data-dir ../voices \
  --output-file question.wav \
  -- "What is your phone number?"

aplay question.wav

arecord -d 5 -f cd -c 1 -r 16000 number.wav
