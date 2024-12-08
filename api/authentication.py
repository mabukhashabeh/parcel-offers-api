import uuid
from datetime import datetime, timedelta
from enum import Enum
from hashlib import sha256
from typing import NamedTuple, Optional

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from jwt.exceptions import InvalidAlgorithmError, InvalidTokenError
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed


class JWTToken(NamedTuple):
    access: str
    refresh: str


class JWTTokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class JWTTokenGenerator:
    algorithm: str = None
    _secret: str = None

    def __init__(self):
        self.algorithm = self.algorithm or "HS256"

    @property
    def secret(self) -> str:
        return self._secret or settings.SECRET_KEY

    @secret.setter
    def secret(self, secret: str):
        self._secret = secret

    def make_tokens(self, user: User) -> JWTToken:
        """
        Create access and refresh tokens for the user.
        """
        now = self._now()
        access_token = self._make_token(
            token_type=JWTTokenType.ACCESS,
            user=user,
            now=now,
            lifetime=settings.CUSTOM_AUTH_JWT["ACCESS_TOKEN_LIFETIME"],
        )
        refresh_token = self._make_token(
            token_type=JWTTokenType.REFRESH,
            user=user,
            now=now,
            lifetime=settings.CUSTOM_AUTH_JWT["REFRESH_TOKEN_LIFETIME"],
        )

        return JWTToken(access=access_token, refresh=refresh_token)

    def _make_token(
        self, token_type: JWTTokenType, user: User, now: datetime, lifetime: timedelta
    ) -> str:
        """
        Generate a token of the specified type (access or refresh) with expiration time.
        """
        exp = now + lifetime
        payload = {
            "token_type": token_type,
            "user_id": str(user.pk),
            "jti": str(uuid.uuid4().hex),  # Unique token ID
            "exp": exp.timestamp(),  # expiry time
            "iat": now.timestamp(),  # issued at time
            "iss": settings.CUSTOM_AUTH_JWT["ISSUER"],  # issuer of the token
        }

        # include user's password and email hash to token secret to enforce re-login on changes.
        key = f"{self.secret}-{user.password}-{sha256(user.email.encode()).hexdigest()}"
        return jwt.encode(payload, key, algorithm=self.algorithm)

    def get_user_by_access_token(self, token: str) -> Optional[User]:
        """
        Validate the access token and return the user.
        """
        return self._get_user_by_token(
            token=token,
            token_type=JWTTokenType.ACCESS,
            timeout=settings.CUSTOM_AUTH_JWT["ACCESS_TOKEN_LIFETIME"],
        )

    def get_user_by_refresh_token(self, token: str) -> Optional[User]:
        """
        Validate the refresh token and return the user.
        """
        return self._get_user_by_token(
            token=token,
            token_type=JWTTokenType.REFRESH,
            timeout=settings.CUSTOM_AUTH_JWT["REFRESH_TOKEN_LIFETIME"],
        )

    def _get_user_by_token(
        self, token: str, token_type: str, timeout: timedelta
    ) -> Optional[User]:
        """
        Validate the token and return the user.

        The token is first decoded without verifying the signature to extract the user ID.
        Then, the token is decoded again with the user's password to verify the signature.

        If the token type does not match the expected type, None is returned.
        If the token is invalid, expired, or the user does not exist, None is returned.
        If the token is valid, the user returned.
        """
        try:
            # Decode the token without verifying the signature
            payload = jwt.decode(
                token, algorithms=[self.algorithm], options={"verify_signature": False}
            )
        except (InvalidAlgorithmError, InvalidTokenError, jwt.ExpiredSignatureError):
            return None

        try:
            user = User.objects.get(pk=payload.get("user_id"), is_active=True)
        except User.DoesNotExist:
            return None

        key = f"{self.secret}-{user.password}-{sha256(user.email.encode()).hexdigest()}"
        try:
            # Validate the token signature with the user's password
            payload = jwt.decode(token, key, algorithms=[self.algorithm])
        except (InvalidAlgorithmError, InvalidTokenError, jwt.ExpiredSignatureError):
            return None

        if (
            payload.get("token_type") != token_type
            or payload.get("iss") != settings.CUSTOM_AUTH_JWT["ISSUER"]
        ):
            return None

        try:
            # Check the expiry time
            exp = datetime.fromtimestamp(payload.get("exp"))
            if (self._now() - exp).total_seconds() > timeout.total_seconds():
                return None
        except ValueError:
            return None

        return user

    def _num_seconds(self, dt: datetime) -> int:
        """
        Return the number of seconds since 2001-01-01.
        """
        return int((dt - datetime(2001, 1, 1)).total_seconds())

    def _now(self) -> datetime:
        return datetime.now()


class JWTAuthentication(BaseAuthentication):
    """
    Custom authentication class that authenticates a user based on their JWT token.
    """

    www_authenticate_realm = "api"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b"jwt":
            return None

        if len(auth) == 1:
            msg = "Invalid JWT header. No credentials provided."
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = "Invalid JWT header. Credentials string should not contain spaces."
            raise AuthenticationFailed(msg)

        try:
            user = jwt_token_generator.get_user_by_access_token(auth[1])
        except (InvalidAlgorithmError, InvalidTokenError, jwt.ExpiredSignatureError):
            msg = "The token is invalid or expired"
            raise AuthenticationFailed(msg)

        if not user:
            msg = "The token is invalid or expired"
            raise AuthenticationFailed(msg)

        return user, None

    def authenticate_header(self, request):
        return 'JWT realm="%s"' % self.www_authenticate_realm


jwt_token_generator = JWTTokenGenerator()
