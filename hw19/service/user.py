import base64
import hashlib
import hmac

from auth.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS

from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one_user(bid)

    def get_all(self):
        return self.dao.get_all_users()

    def get_user_by_username(self, username):
        return self.dao.get_user_by_username(username)

    def create(self, user_d):
        user_d["password"] = self.get_hash(user_d.get("password"))
        return self.dao.create(user_d)

    def update(self, user_d):
        user_d["password"] = self.get_hash(user_d.get("password"))
        return self.dao.update(user_d)

    def delete(self, bid):
        return self.dao.delete(bid)

    def get_hash(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    def compare_passwords(self, password_hash, other_password) -> bool:
        """ Проверка пароля из request, пароля в БД """
        return hmac.compare_digest(
            base64.b64decode(password_hash),
            hashlib.pbkdf2_hmac(
                'sha256',
                other_password.encode('utf-8'),
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS)
        )
