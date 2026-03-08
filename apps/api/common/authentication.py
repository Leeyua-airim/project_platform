# apps/api/common/authentication.py
# Supabase access token(JWT)을 검증해서
# DRF의 request.user / request.auth 로 연결하는 인증 클래스

from typing import Any, Dict

import jwt
from django.conf import settings
from rest_framework import authentication, exceptions


class SupabaseUser:
    """
    Django 기본 User 모델을 아직 쓰지 않는 MVP 단계용 사용자 객체

    역할:
    - JWT payload 안의 사용자 식별 정보를 보관
    - request.user.id, request.user.email 형태로 접근 가능하게 함
    """
    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload
        self.id = payload.get("sub")
        self.email = payload.get("email")
        self.is_authenticated = True

    def __str__(self) -> str:
        return self.email or self.id or "supabase-user"


class SupabaseJWTAuthentication(authentication.BaseAuthentication):
    """
    Authorization: Bearer <token> 헤더를 읽고
    Supabase JWKS로 JWT 서명을 검증하는 DRF 인증 클래스
    """

    def authenticate(self, request):
        # 요청 헤더에서 Authorization 값을 읽음
        auth_header = authentication.get_authorization_header(request).decode("utf-8")

        # 인증 헤더가 없으면 인증되지 않은 요청으로 처리
        if not auth_header:
            return None

        parts = auth_header.split()

        # Authorization 헤더는 'Bearer <token>' 형식이어야 함
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise exceptions.AuthenticationFailed("Invalid Authorization header format")

        token = parts[1]
        payload = self._decode_token(token)

        # 검증된 payload를 request.user에 연결
        return SupabaseUser(payload), token

    def _decode_token(self, token: str) -> Dict[str, Any]:
        # settings.py에 정의한 Supabase JWKS URL을 읽음
        jwks_url = getattr(settings, "SUPABASE_JWKS_URL", "")
        if not jwks_url:
            raise exceptions.AuthenticationFailed("SUPABASE_JWKS_URL is not configured")

        try:
            # PyJWT가 JWKS 조회와 kid에 맞는 서명 키 선택을 처리
            jwk_client = jwt.PyJWKClient(jwks_url)
            signing_key = jwk_client.get_signing_key_from_jwt(token)

            # 선택된 공개키로 access token 서명을 검증
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256", "ES256"],
                options={"verify_aud": False},
            )
            return payload

        except jwt.ExpiredSignatureError as exc:
            raise exceptions.AuthenticationFailed("Token expired") from exc
        except jwt.InvalidSignatureError as exc:
            raise exceptions.AuthenticationFailed(f"Invalid signature: {exc}") from exc
        except jwt.DecodeError as exc:
            raise exceptions.AuthenticationFailed(f"Decode error: {exc}") from exc
        except jwt.InvalidAudienceError as exc:
            raise exceptions.AuthenticationFailed(f"Invalid audience: {exc}") from exc
        except jwt.InvalidIssuerError as exc:
            raise exceptions.AuthenticationFailed(f"Invalid issuer: {exc}") from exc
        except jwt.InvalidTokenError as exc:
            raise exceptions.AuthenticationFailed(f"Invalid token detail: {exc}") from exc
        except Exception as exc:
            raise exceptions.AuthenticationFailed(f"JWT verification failed: {exc}") from exc