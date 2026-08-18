# JOBOS backend image for Render (and any Docker host).
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

COPY backend/app ./app

EXPOSE 8000

CMD ["sh", "-c", "python -m app.seed && gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT app.main:app"]
