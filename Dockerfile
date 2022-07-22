# Pull base image
FROM python:3.10.4

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/
COPY requirements.txt requirements.txt
# Install dependencies
RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8088