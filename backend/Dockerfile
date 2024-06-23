# We use the official Python image as the base image
# We specify the Python version to use, so it's more predictable
# We use the Alpine version to keep the image size small
FROM python:3.12-alpine

# We set the working directory in the container
# All subsequent commands will be run in this directory
WORKDIR /app

# We install the required libraries first to leverage Docker's cache
# We don't need to install the dev dependencies in requirements-dev.txt
# And we don't need pip to cache the packages in the Docker image (hence --no-cache-dir)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Flask app in production mode
ENV FLASK_DEBUG 0
ENV FLASK_ENV production

# The default environment variable for the database file path
ENV DB_PATH /data
# We create a volume for the database file
# This way, the database file will persist even if the container is removed
VOLUME ${DB_PATH}

# Gunicorn config, irrelavant for Flask development server or if you're using a different WSGI server
ENV GUNICORN_HOST 0.0.0.0
ENV GUNICORN_PORT 8080
ENV GUNICORN_WORKERS 4
ENV GUNICORN_CMD_ARGS "--bind=${GUNICORN_HOST}:${GUNICORN_PORT} --workers=${GUNICORN_WORKERS}"

# After everything is installed, we copy the source code
COPY . /app

# We expose the port that Gunicorn will listen on
EXPOSE ${GUNICORN_PORT}

# Finally, we run Gunicorn (instead of Flask's development server)
# We don't need to specify the host and port, as we've done that with the environment variables
CMD [ "gunicorn", "main:app" ]
