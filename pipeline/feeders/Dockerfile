FROM python:3.11-slim
WORKDIR /app

RUN pip install --no-cache-dir requests

COPY feed_loop.py .
COPY urlhaus.py .
COPY phishtank.py .
COPY tranco.py .

ENV OUT_DIR=/data
VOLUME ["/data"]

CMD ["python", "feed_loop.py"]