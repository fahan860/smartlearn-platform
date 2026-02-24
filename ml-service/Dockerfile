FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY main.py ./main.py
COPY config.py ./config.py

ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=/app/models/recommender.pkl
ENV PYTHONPATH=/app/src

RUN useradd --create-home --shell /usr/sbin/nologin appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8001

CMD ["python", "main.py"]
