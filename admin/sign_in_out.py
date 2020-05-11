from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from database.models import A
import json
# 登录处理
def signin(request):
    # 从 HTTP POST 请求中获取系统管理员账号、密码参数
    request.params = json.loads(request.body)
    adminId = request.params['adminId']
    passWord = request.params['password']

    try:
        # 根据学号从数据库学生表中找到相应的学生记录
        admin = A.objects.get(gh=adminId)
    except A.DoesNotExist:
        return JsonResponse({
            'ret': 1,
            'msg': f'工号 为`{adminId}`的管理员不存在'
        })
    userName = admin.gh
    # 使用 Django auth 库里面的方法校验用户名、密码
    user = authenticate(username=userName, password=passWord)
    # 如果能找到用户，并且密码正确
    if user is not None:
        if user.is_active:
            login(request, user)
            # 在session中存入用户类型
            request.session['member_id'] = adminId
            return JsonResponse({'ret': 0})
        else:
            return JsonResponse({'ret': 0, 'msg': '用户已经被禁用'})
    # 否则就是用户名、密码有误
    else:
        return JsonResponse({'ret': 1, 'msg': '密码错误'})


# 登出处理
def signout(request):
    # 使用登出方法
    logout(request)
    return JsonResponse({'ret': 0})