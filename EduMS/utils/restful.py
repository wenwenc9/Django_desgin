from django.http import JsonResponse
import json


class HttpCode(object):
    ok = 200
    unautherror = 401
    paramserror = 400
    servererror = 500

def restful_result(code,message,data,inner=False):
    result = {"code": code, "message": message, "data": data or {}}
    if inner:
        return json.dumps(result)
    else:
        return JsonResponse(result)

def success(message="", data=None, inner=False):
    return restful_result(code=HttpCode.ok, message=message, data=data, inner=inner)

def unauth_error(message="", inner=False):
    return restful_result(code=HttpCode.unautherror, message=message, data=None, inner=inner)

def params_error(message="", inner=False):
    return restful_result(code=HttpCode.paramserror, message=message, data=None, inner=inner)

def server_error(message="", inner=False):
    return restful_result(code=HttpCode.servererror, message=message or '服务器内部错误', data=None, inner=inner)