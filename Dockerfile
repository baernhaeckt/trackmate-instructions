FROM python:3.12-slim

# tell the host we are running on port 8000
# note: we intentionally run on a port >= 1024 here because lower ports needed special treatment
EXPOSE 8000

# keep Python from generating .pyc files
# note: those files won't be needed in a container where a process is run only once.
ENV PYTHONDONTWRITEBYTECODE=1

# turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# install pip requirements
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# set workdir and copy app to image
WORKDIR /app
COPY . /app

# define the entry point
ENTRYPOINT uvicorn main:app \
    --host="0.0.0.0" \
    --port=8000 \
    --log-level warning \
    --no-proxy-headers \
    --no-server-header \
    --no-date-header \
    --timeout-keep-alive 120 \
    --timeout-graceful-shutdown 120

