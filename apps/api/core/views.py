from rest_framework.decorators import api_view
from rest_framework.response import Response

from .tasks import ping_task

@api_view(["GET"])
def health(request):
    """헬스체크: 서버가 살아있는지 확인."""
    return Response({"status": "ok"})

@api_view(["POST"])
def enqueue_ping(request):
    """ping_task를 큐에 넣어서 Celery/Redis가 정상적으로 동작하는지 확인."""
    async_result = ping_task.delay()  # ping_task를 비동기로 실행
    return Response({"task_id": async_result.id})