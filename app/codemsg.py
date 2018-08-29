# -*- coding: utf-8 -*-
class CodeMsg:
    _code_msg = {
        "000000": "成功",
        "400000": "错误请求",
        "400001": "请求无效, 缺少必传参数",
        "401000": "未授权",
        "401001": "用户不存在或密码错误",
        "401002": "token或uid缺少",
        "401003": "token过期",
        "401004": "token错误",
        "403000": "禁止访问",
        "404000": "找不到",
        "500000": "内部服务器错误",
        "502000": "网关错误",
        "503000": "无法获得服务",
        "600100": "用户不存在",
        "600101": "用户信息更新失败",
    }

    def __init__(self):
        pass

    @classmethod
    def get_msg(cls, code):
        return cls._code_msg.get(code, "未知错误")
