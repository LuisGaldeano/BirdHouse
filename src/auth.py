from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
from fastapi.security.utils import get_authorization_scheme_param
from starlette import status

from settings import API_KEY

AUTH_HEADER = APIKeyHeader(name='Authorization')


def api_key_auth(auth_value: str = Depends(AUTH_HEADER)) -> None:
    scheme, param = get_authorization_scheme_param(auth_value)

    if scheme.lower() != "bearer" or param != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Key",
        )
