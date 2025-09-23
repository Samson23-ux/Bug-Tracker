from fastapi import FastAPI
from app.middleware import LogRequestMiddleware
from app.services.errors import UserExistError, UsernameError, PasswordError
from app.services.errors import UserNotFoundError, BugNotFoundError
from app.services.errors import user_exist_handler, invalid_username_handler, invalid_password_handler
from app.services.errors import user_not_found_handler, bug_not_found_handler
from app.routers import auth, users, bugs

app = FastAPI(title='Bugs Management')

#routers
app.include_router(auth.router, prefix='/auth', tags=['SignUp/SignIn'])
app.include_router(users.router, prefix='/users', tags=['Users'])
app.include_router(bugs.router, prefix='/bugs', tags=['Bugs'])

#middleware
app.add_middleware(LogRequestMiddleware)

#exception handlers
app.add_exception_handler(UserExistError, user_exist_handler)
app.add_exception_handler(UsernameError, invalid_username_handler)
app.add_exception_handler(PasswordError, invalid_password_handler)
app.add_exception_handler(UserNotFoundError, user_not_found_handler)
app.add_exception_handler(BugNotFoundError, bug_not_found_handler)
