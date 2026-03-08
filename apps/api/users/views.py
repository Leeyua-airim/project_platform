# apps/api/users/views.py
# 현재 로그인한 Supabase 사용자 정보를 반환하는 API 뷰

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class MeView(APIView):
    # 인증된 사용자만 접근 가능
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        authentication.py 에서 만든 SupabaseUser 객체를 사용해
        현재 로그인 사용자 정보를 반환
        """
        return Response(
            {
                "id": getattr(request.user, "id", None),
                "email": getattr(request.user, "email", None),
                "claims": getattr(request.user, "payload", {}),
            }
        )