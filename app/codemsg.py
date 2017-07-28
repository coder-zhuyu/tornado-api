# -*- coding: utf-8 -*-
class CodeMsg:
    _code_msg = {
        "000000": u"成功",
        "400000": u"错误请求",
        "400001": u"请求无效, 缺少必传参数",
        "401000": u"未授权",
        "401001": u"用户不存在或密码错误",
        "403000": u"禁止访问",
        "404000": u"找不到",
        "500000": u"内部服务器错误 ",
    }

    def __init__(self):
        pass

    @classmethod
    def get_msg(cls, code):
        return cls._code_msg.get(code, u"未知错误")
