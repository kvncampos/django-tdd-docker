# Pull official base image
FROM python:3.12.4-slim-bookworm

# Set working directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Copy Poetry files
COPY ../pyproject.toml ../poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Add app
COPY ../app ./

# Command to run your application (adjust as needed)
# CMD ["python", "your_script.py"]
