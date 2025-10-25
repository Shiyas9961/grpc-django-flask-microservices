FROM python:3.13-alpine

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

EXPOSE 50051

CMD ["python", "grpc_server/server.py"]
