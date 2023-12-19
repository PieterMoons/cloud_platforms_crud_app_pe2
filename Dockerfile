
FROM python:latest

# Install dependencies
WORKDIR /app
COPY . .

# Install python, PIP and requirements
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["gunicorn","--config", "gunicorn_config.py", "app:app"]




