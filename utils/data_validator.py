from functools import wraps
from typing import List, Type, get_origin

from flask import request
from pydantic import BaseModel, ValidationError


class DataValidator:

    def __init__(self, model: Type[BaseModel] | Type[list], is_list: bool = False):
        self.model = model
        self.is_list = is_list

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = None

            if not request.is_json:
                return

            if self.is_list:
                if type(request.json) != list:
                    raise Exception("Invalid payload")

                data = []
                for d in request.json:
                    model_data = self.model(**d)
                    data.append(model_data)
            else:
                data = self.model(**request.json)

            return f(data, *args, **kwargs)

        return wrapper
