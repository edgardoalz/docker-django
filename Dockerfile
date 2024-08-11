# Parent image
FROM python:3.11-alpine

# Working directory
RUN mkdir -p /app
WORKDIR /app

# Environment variables
ENV PORT=8000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# User and group
RUN addgroup -S app \
    && adduser app -S -G app

# Install system dependencies
# && apk add netcat-openbsd \
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add mariadb-dev \
    && apk add tini \
    && apk add curl \
    && rm -rf /var/cache/apk/*

# Install python dependencies
RUN pip install --upgrade pip
COPY ./requirements*.txt .
RUN pip install -r requirements-runtime.txt

# Setup runtime scripts
COPY ./scripts/*.sh /app/
RUN sed -i 's/\r$//g' /app/*.sh
RUN chmod +x /app/*.sh

# Copy project
COPY . /app

# Change owner all the files to the app user
RUN chown -R app:app /app

# Change to the app user
USER app

# Run entrypoint.sh
ENTRYPOINT ["/sbin/tini", "-g", "--", "/app/docker-entrypoint.sh"]

EXPOSE $PORT

# Run command
CMD ["/app/django-start.sh"]