import json

from flask import request
from flask_restx import Resource, Namespace

from auth.helpers import auth_required, admin_required
from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UserView(Resource):
    @admin_required
    def get(self):
        all_users = user_service.get_all()
        res = UserSchema(many=True).dump(all_users)
        return res, 200

    def post(self):
        req_json = json.loads(request.data)
        user = user_service.create(req_json)
        return f"Пользователь {user.username} добавлен", 201, {"location": f"/users/{user.id}"}


@user_ns.route('/<int:bid>')
class UserView(Resource):
    @admin_required
    def get(self, bid):
        b = user_service.get_one(bid)
        sm_d = UserSchema().dump(b)
        return sm_d, 200

    @admin_required
    def put(self, bid):
        req_json = json.loads(request.data)
        if "id" not in req_json:
            req_json["id"] = bid
        user_service.update(req_json)
        return "", 204

    @auth_required
    @admin_required  # Удалять пользователя может только Admin
    def delete(self, bid):
        user_service.delete(bid)
        return "", 204
