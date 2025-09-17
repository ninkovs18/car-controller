# ---- Base image ----
FROM python:3.11-slim

# ---- Set working directory ----
WORKDIR /app

# ---- Install system deps (ako treba Pillow i sl.) ----
RUN apt-get update && apt-get install -y \
    libjpeg-dev zlib1g-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# ---- Copy dependencies ----
COPY requirements.txt .

# ---- Install dependencies ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy app code ----
COPY . .

# ---- Expose FastAPI port ----
EXPOSE 8080

# ---- Run FastAPI ----
CMD exec uvicorn app:app --host 0.0.0.0 --port $PORT
