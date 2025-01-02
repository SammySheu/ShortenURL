FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shortenURL shortenURL
COPY templates templates
COPY manage.py .

EXPOSE 8000

RUN echo '#!/bin/sh\n\
python manage.py migrate\n\
python manage.py setup_initial_data\n\
python manage.py runserver 0.0.0.0:8000\n'\
> /app/entrypoint.sh \
&& chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]