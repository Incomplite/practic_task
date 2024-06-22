FROM python:3.10.13-slim-bookworm

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y \
    binutils \
    gdal-bin \
    libproj-dev \
    libgeos-dev \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
WORKDIR /app/geo_buildings_project
