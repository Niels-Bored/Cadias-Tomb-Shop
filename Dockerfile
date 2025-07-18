#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "apply-templates.sh"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#

# Use Python 3.12 slim image
FROM python:3.12-slim

# Load env vars from caprover settings
ARG ENV

ARG SECRET_KEY
ARG DEBUG
ARG ALLOWED_HOSTS
ARG HOST

ARG DB_ENGINE
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT

ARG USE_SQLITE

ARG TEST_HEADLESS


ARG STORAGE_AWS
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_STORAGE_BUCKET_NAME

ARG EMAIL_HOST
ARG EMAIL_PORT
ARG EMAIL_HOST_USER
ARG EMAIL_HOST_PASSWORD
ARG EMAIL_USE_SSL

ARG STRIPE_API_HOST
ARG STRIPE_API_USER

# Load env vars from caprover settings
ENV ENV=${ENV}
ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=${DEBUG}
ENV ALLOWED_HOSTS=${ALLOWED_HOSTS}
ENV HOST=${HOST}

ENV DB_ENGINE=${DB_ENGINE}
ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}

ENV USE_SQLITE=${USE_SQLITE}

ENV TEST_HEADLESS=${TEST_HEADLESS}

ENV STORAGE_AWS=${STORAGE_AWS}
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV AWS_STORAGE_BUCKET_NAME=${AWS_STORAGE_BUCKET_NAME}

ENV EMAIL_HOST=${EMAIL_HOST}
ENV EMAIL_PORT=${EMAIL_PORT}
ENV EMAIL_HOST_USER=${EMAIL_HOST_USER}
ENV EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}
ENV EMAIL_USE_SSL=${EMAIL_USE_SSL}

ENV STRIPE_API_HOST=${STRIPE_API_HOST}
ENV STRIPE_API_USER=${STRIPE_API_USER}

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app/

# Install system dependencies (e.g., for PostgreSQL support)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files and migrate database
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Expose the port that Django/Gunicorn will run on
EXPOSE 80

# Command to run Gunicorn with the WSGI application for production
CMD ["gunicorn", "--bind", "0.0.0.0:80", "cadiashop.wsgi:application"]