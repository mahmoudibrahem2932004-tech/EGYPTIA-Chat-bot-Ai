#!/bin/bash
cd /app

echo "📦 Checking for trained model..."
if [ ! -f models/*.tar.gz ]; then
    echo "🔄 No model found. Training Rasa model..."
    rasa train
    echo "✅ Training complete!"
else
    echo "✅ Model found. Skipping training."
fi

echo "🚀 Starting Rasa actions on port 5055..."
rasa run actions --port 5055 &
sleep 5

echo "🚀 Starting Rasa server on port 5005..."
rasa run --enable-api --cors "*" -p 5005 &
sleep 10

echo "🚀 Starting HTTP server for HTML interface on port 7860..."
python -m http.server 7860 --bind 0.0.0.0