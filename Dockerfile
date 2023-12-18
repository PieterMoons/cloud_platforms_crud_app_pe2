
FROM python:latest

# Install dependencies
WORKDIR /app
COPY . .

# Install python, PIP and requirements
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt


CMD ["gunicorn","app:app","--bind","0.0.0.0:8000","--workers","4"]




