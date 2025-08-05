FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --nochache-dir -r requirements.txt

COPY app/ ./app/
COPY run.py .

ENV FLASK_APP=app/frontend/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBFFERED=1

EXPOSE 5000

RUN python app/backend/generate_db.py

CMD ["flask", "run"]
