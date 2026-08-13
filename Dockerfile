# ---- Build stage ----
    FROM python:3.11-slim AS build

    WORKDIR /app
    
    COPY requirements.txt .
    RUN pip install --no-cache-dir --user -r requirements.txt
    
    # ---- Runtime stage ----
    FROM python:3.11-slim
    
    WORKDIR /app
    
    RUN useradd --create-home --shell /bin/bash app
    
    COPY --from=build /root/.local /home/app/.local
    
    COPY app ./app
    COPY frontend ./frontend
    
    ENV PATH=/home/app/.local/bin:$PATH
    ENV PYTHONPATH=/app
    
    RUN chown -R app:app /app /home/app/.local
    
    USER app
    
    EXPOSE 8000
    
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]