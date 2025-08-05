FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#COPY . .
COPY app/ ./app/
COPY run.py .

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

EXPOSE 5000

#RUN python backend/generate_db.py

RUN ls -R /app/app/backend
CMD ["flask", "run"]

#CMD ["sh", "-c", "python app/backend/generate_db.py && flask run"]