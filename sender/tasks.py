from celery import Celery

app = Celery('sender.tasks', broker='redis://:jjsja7123jdasdkk21238882jjejq@localhost:6377/0')
app.conf['worker_prefetch_multiplier'] = 10


@app.task(queue='celery', name='other_task')
def start_spider(spider_name):
    print(spider_name)
    # subject, message, destination = 'Test subject', 'This is the message', 'rota199804@gmail.com'
    # msg = MIMEText(message, 'plain')
    # msg['Subject'] = subject
    #
    # with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
    #     server.starttls()
    #     server.login(EMAIL_FROM, EMAIL_HOST_PASSWORD)
    #     server.sendmail(EMAIL_FROM, destination, msg.as_string())
    for i in range(1, 100):
        print(i)