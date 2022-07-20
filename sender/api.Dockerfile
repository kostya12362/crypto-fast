FROM python:3.9
WORKDIR /auth

COPY ./requirements.txt /auth/requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /auth/requirements.txt
COPY . .
EXPOSE 5005
CMD ["python", "main.py"]