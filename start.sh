#!/bin/bash
cd /app
echo "تشغيل Rasa actions..."
rasa run actions &
echo "تشغيل Rasa server..."
rasa run --enable-api --cors "*" -p 5005 &
echo "تشغيل واجهة Gradio..."
python app.py &
echo "تشغيل خادم HTTP لملف HTML..."
python -m http.server 7860 --bind 0.0.0.0