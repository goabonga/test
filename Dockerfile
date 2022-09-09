# Use a specific version of the official Python 3.12 image as the base image
# This ensures that our application runs on Python 3.12
FROM python:3.12

# Set the working directory inside the container to /app/
# All subsequent commands will be executed inside this directory
WORKDIR /app/

# Install Poetry (Python dependency management and packaging tool)
# The POETRY_HOME environment variable specifies where Poetry will be installed
# The 'ln -s' command creates a symbolic link to Poetry in the global PATH
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false
