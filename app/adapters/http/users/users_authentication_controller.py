import logging

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.adapters.http.auth.jwt_user_signer import JwtUserSigner
from app.adapters.http.auth.output.token import Token
from app.dependencies.dependencies import user_auth_usecases_dependency
from app.domain.users.command.user_credentials_command import UserCredentialsCommand
from app.domain.users.usecases.user_authentication_usecases import (
    UserAuthenticationUseCases,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_auth_usecases: UserAuthenticationUseCases = Depends(
        user_auth_usecases_dependency
    ),
):
    user = user_auth_usecases.find_by_credentials(
        UserCredentialsCommand(username=form_data.username, password=form_data.password)
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return Token(
        access_token=JwtUserSigner().create_access_token(user.username),
        token_type='bearer',
    )
