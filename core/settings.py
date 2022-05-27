import os

RMQ_URL_CONNECTION_STR = os.getenv('RMQ_URL_CONNECTION_STR', 'amqp://myuser:mypassword@localhost:5672/?heartbeat=3600')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6377)
REDIS_DB = os.getenv('REDIS_DB')
REDIS_PASS = os.getenv('REDIS_PASS', 'jjsja7123jdasdkk21238882jjejq')

REDIS_SESSION_BLACK_LIST = os.getenv('REDIS_SESSION_BLACK_LIST', 'session_black_list')
