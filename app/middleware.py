import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.utils import write_logs

class LogRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method, url = request.method, request.url
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        text = f'Method: {method}, URL: {url}, Time: {process_time}\n'
        await write_logs('logs.txt', text)
        response.headers['X-App-Name'] = 'Taskify'
        return response
