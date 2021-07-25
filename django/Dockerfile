# pull the official docker image
FROM python:3.9-buster

EXPOSE 8000

# set work directory
WORKDIR /django

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gdal-bin
COPY requirements.txt .
COPY requirements.dev.txt .
RUN pip install -U pip && \
    pip install -r requirements.dev.txt

# copy project
COPY . .

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /django
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# File wsgi.py was not found in subfolder: 'Website'. Please enter the Python path to wsgi file.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "trainerdex.wsgi"]