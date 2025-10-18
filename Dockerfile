FROM python:3.11-slim
WORKDIR /app
COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY app /app
ENV PORT=5000
EXPOSE 5000
CMD ["python", "app.py"]
