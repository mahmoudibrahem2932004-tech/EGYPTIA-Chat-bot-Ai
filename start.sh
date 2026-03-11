#!/bin/bash
cd /app
rasa run actions &
rasa run --enable-api --cors "*" -p 7860