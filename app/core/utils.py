import aiofiles
import json
import hashlib
# from pathlib import Path

async def read_json(filename: str) -> list[dict]:
    try:
        async with aiofiles.open(f'app\\data\\{filename}', 'r') as file:
            user_data = await file.read()
            data = json.loads(user_data)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    return data

async def write_json(filename: str, data: list[dict]):
    async with aiofiles.open(f'app\\data\\{filename}', 'w') as file:
        user_data = json.dumps(data, indent=4)
        await file.write(user_data)

async def write_logs(filename: str, data):
    async with aiofiles.open(f'app\\data\\{filename}', 'a') as file:
        await file.write(data)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
