from app.auth.dependencies import auth_backend, fastapi_users
from app.auth.schemas import UserCreate, UserRead, UserUpdate

auth_jwt_router = fastapi_users.get_auth_router(auth_backend)
auth_register_router = fastapi_users.get_register_router(UserRead, UserCreate)
auth_reset_password_router = fastapi_users.get_reset_password_router()
auth_verify_router = fastapi_users.get_verify_router(UserRead)
users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
