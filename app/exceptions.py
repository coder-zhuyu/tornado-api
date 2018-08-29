# -*- coding: utf-8 -*-
class ValidationError(ValueError):
    pass


class UserIDException(Exception):
    def __init__(self):
        Exception.__init__(self, 'user_id not equal')
