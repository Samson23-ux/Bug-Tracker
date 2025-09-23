import secrets, string
from app.core.utils import read_json, write_json, hash_password
from app.services.errors import UserExistError, UserNotFoundError
from app.services.errors import UsernameError, PasswordError
from app.schemas.users import Account

class UserService:
    def generate_token(self) -> str:
        token = ''
        char = string.ascii_letters + string.digits
        for _ in range(9):
            token += secrets.choice(char)
        return token

    def remove_password(
            self,
            user: dict = None,
            users: list[dict] = None
    ) -> dict:
        if users is not None:
            for usr in users:
                del usr['password']
            return users

        if user is not None:
            del user['password']
            return user

    async def is_user_exist(self, username: str) -> bool:
        users = await read_json('users.json')
        for user in users:
            username = username.lower().strip()
            if username == user['username'].lower().strip():
                return True
        return False

    def get_user_by_id(self, user_id: str, users: list[dict]) -> dict:
        for user in users:
            if user['id'] == user_id:
                return user

    async def get_users(self, role: str | None = None) -> list[dict]:
        users = await read_json('users.json')
        if role is not None:
            role = role.lower().strip()
            users = [usr for usr in users if role == usr['role'].lower().strip()]

        return users

    async def get_user(self, username: str) -> dict:
        users = await read_json('users.json')

        for user in users:
            username = username.lower().strip()
            if username == user['username'].lower().strip():
                return user
        raise UserNotFoundError('User not found!')

    async def create_user(self, user: dict) -> dict:
        user_acc = user.copy()
        users = await read_json('users.json')

        if await self.is_user_exist(user_acc['username']):
            raise UserExistError('Username already exist!')

        user_model = Account(
            id=str(len(users) + 1),
            **user
        )
        user_acc = user_model.model_dump()
        user_acc['password'] = hash_password(user_acc['password'])

        users.append(user_acc)

        await write_json('users.json', users)

        return user_acc

    async def sign_user_in(self, user_id: str, username: str, password: str) -> dict:
        username = username.lower().strip()
        users = await read_json('users.json')
        user = self.get_user_by_id(user_id, users)

        if user is None:
            raise UserNotFoundError('User not found!')

        if user['username'].lower().strip() != username:
            raise UsernameError('Invalid username!')

        if user['password'] != hash_password(password):
            raise PasswordError('Invalid password!')

        user['token'] = self.generate_token()

        await write_json('users.json', users)

        return user

    async def sign_user_out(self, user_id: str) -> dict:
        users = await read_json('users.json')
        user = self.get_user_by_id(user_id, users)

        if user is None:
            raise UserNotFoundError('User not found!')

        del user['token']
        await write_json('users.json', users)

        return user

    async def update_account(self, user_id: str, account_update: dict, password: str) -> dict:
        users = await read_json('users.json')
        user = self.get_user_by_id(user_id, users)

        if user is None:
            raise UserNotFoundError('User not found!')

        if hash_password(password) != user['password']:
            raise PasswordError('Invalid password!')

        for key, update in account_update.items():
            for k, _ in user.items():
                if key == k:
                    user[k] = update
                    continue
        await write_json('users.json', users)

        return user

    async def update_password(self, user_id: str, curr_password: str, new_password: str) -> dict:
        users = await read_json('users.json')
        user = self.get_user_by_id(user_id, users)

        if user is None:
            raise UserNotFoundError('User not found!')

        if user['password'] != hash_password(curr_password):
            raise PasswordError('Invalid password!')

        user['password'] = hash_password(new_password)

        await write_json('users.json', users)

        return user

    async def delete_account(self, user_id: str):
        users = await read_json('users.json')
        user = self.get_user_by_id(user_id, users)

        if user is None:
            raise UserNotFoundError('User not found!')

        users.remove(user)

        await write_json('users.json', users)

user_service = UserService()
