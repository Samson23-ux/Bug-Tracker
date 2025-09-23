from fastapi import Request
from fastapi.responses import JSONResponse

#errors
class UserExistError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class PasswordError(Exception):
    pass

class UsernameError(Exception):
    pass

class BugNotFoundError(Exception):
    pass

#handlers
def user_exist_handler(request: Request, exc: UserExistError):
    return JSONResponse(
        status_code=400,
        content='Username already exist!'
)

def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content='User not Found!'
)

def invalid_username_handler(request: Request, exc: UsernameError):
    return JSONResponse(
        status_code=400,
        content='Invalid username!'
)

def invalid_password_handler(request: Request, exc: PasswordError):
    return JSONResponse(
        status_code=400,
        content='Invalid password!'
)

def bug_not_found_handler(request: Request, exc: BugNotFoundError):
    return JSONResponse(
        status_code=404,
        content='Bug not found!'
)
