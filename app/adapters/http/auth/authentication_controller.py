import logging

from fastapi import Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm

from app.adapters.http.auth.jwt_user_signer import JwtUserSigner
from app.adapters.http.auth.output.token import Token
from app.dependencies.dependencies import (
    user_auth_usecases_dependency,
    jwt_user_signer_dependency,
)
from app.domain.users.command.user_credentials_command import UserCredentialsCommand
from app.domain.users.usecases.user_authentication_usecases import (
    UserAuthenticationUseCases,
)

router = APIRouter(tags=["auth"])
logger = logging.getLogger(__name__)


@router.post(
    "/token", response_model=Token, status_code=status.HTTP_201_CREATED,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_auth_usecases: UserAuthenticationUseCases = Depends(
        user_auth_usecases_dependency
    ),
    jwt_user_signer: JwtUserSigner = Depends(jwt_user_signer_dependency),
):
    user = user_auth_usecases.find_by_credentials(
        UserCredentialsCommand(username=form_data.username, password=form_data.password)
    )

    return Token(
        access_token=jwt_user_signer.create_access_token(user.username),
        token_type='bearer',
    )
