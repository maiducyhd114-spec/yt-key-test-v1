FROM python:3.11-slim
WORKDIR /app
COPY server.py ./server.py
COPY templates ./templates
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir flask gunicorn
ENV PORT=5000
EXPOSE 5000
CMD ["python","server.py"]
