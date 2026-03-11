#!/bin/bash
cd /app
rasa train
rasa run actions &
rasa run --enable-api --cors "*" -p 7860