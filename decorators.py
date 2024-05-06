from functools import wraps

import jwt
from flask import request, make_response, jsonify, current_app, abort

from baked_response import BakedResponse
from database.database_handler import DatabaseHandler


def authorization(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            try:
                token = request.headers["Authorization"].split(" ")[1]
            except Exception as e:
                response = BakedResponse.get_baked_401_response()
                return make_response(jsonify(response), 401)
        if not token:
            response = BakedResponse.get_baked_401_response()
            return make_response(jsonify(response), 401)
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            database_handler = DatabaseHandler()
            current_user = database_handler.get_customer(data["user_email"])
            if current_user is None:
                response = BakedResponse.get_baked_401_response()
                return make_response(jsonify(response), 401)
            if not current_user[3]:
                response = BakedResponse.get_baked_401_response()
                return make_response(jsonify(response), 401)
        except Exception as e:
            response = BakedResponse.get_baked_500_response()
            return make_response(jsonify(response), 500)
