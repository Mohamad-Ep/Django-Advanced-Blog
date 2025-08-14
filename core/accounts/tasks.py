from celery import shared_task
from time import sleep

# __________________________________________________________


@shared_task
def get_send_email():
    sleep(4)
    print("Ths First page is Active")


# __________________________________________________________
