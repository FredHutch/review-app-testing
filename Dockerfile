# based on https://rye-up.com/guide/docker/
FROM python:3.12.0-slim


WORKDIR /app
COPY requirements.lock ./
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

COPY src .

EXPOSE 5050
# not a production server but this is just a demo
CMD python3 -m review_app_testing.app


