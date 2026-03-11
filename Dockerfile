FROM rasa/rasa:3.6.2

WORKDIR /app

COPY . /app

USER root

RUN chmod +x start.sh

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860
EXPOSE 5005
EXPOSE 5055

CMD ["./start.sh"]