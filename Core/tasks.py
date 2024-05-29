from celery import shared_task


@shared_task(bind=True)
def add(x,y):
    z=4+4
    return z

    # return "Done"
