FROM python:3.9-slim
WORKDIR /sender

COPY ./requirements.txt /sender/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /sender/requirements.txt
COPY . .
RUN chmod 777 /sender/celery_worker.sh
CMD /sender/celery_worker.sh