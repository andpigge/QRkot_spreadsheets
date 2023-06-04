from fastapi import APIRouter, HTTPException

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

""" Аутентификация токена. """
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth']
)

""" Регистрация пользователя. """
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth']
)

""" Управление пользователем. """
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users']
)


@router.delete('/users/{id}',
               tags=['users'],
               deprecated=True)
def delete_user(id: str):
    """ Не используйте удаление, деактивируйте пользователей. """

    raise HTTPException(
        status_code=405,
        detail="Удаление пользователей запрещено!"
    )
