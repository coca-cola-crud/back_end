from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from database.models import S
from database.models import T
import json
# 登录处理
def signin(request):
    request.params = json.loads(request.body)
    teacherId = request.params['teacherid']
    passWord = request.params['password']
    print(teacherId)
    try:
        # 根据工号从数据库教师表中找到相应的教师记录
        teacher = T.objects.get(gh=teacherId)
    except T.DoesNotExist:
        return JsonResponse({
            'ret': 1,
            'msg': f'工号为`{teacherId}`的老师不存在'
        })
    userName = teacher.gh
    # 使用 Django auth 库里面的方法校验用户名、密码
    user = authenticate(username=userName, password=passWord)
    # 如果能找到教师，并且密码正确
    if user is not None:
        if user.is_active:
            login(request, user)
            # 在session中存入用户类型
            request.session['member_id'] = teacherId
            return JsonResponse({'ret': 0})
        else:
            return JsonResponse({'ret': 0, 'msg': '用户已经被禁用'})
    # 否则就是密码有误
    else:
        return JsonResponse({'ret': 1, 'msg': '密码错误'})

# 登出处理
def signout(request):
    # 使用登出方法
    logout(request)
    return JsonResponse({'ret': 0})