FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
WORKDIR /auth

COPY ./requirements.txt /auth/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /auth/requirements.txt
COPY . .
RUN chmod 777 /auth/db.sh
CMD /auth/db.sh


CMD ["python", "main.py"]
