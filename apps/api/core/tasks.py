from celery import shared_task

@shared_task
def ping_task() -> str:
    """
    Celery/Redis 큐 동작을 확인하기 위한 더미 작업.
    - 큐에 정상적으로 들어가고 worker에서 실행되는지 확인한다.
    """
    return "pong"