from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from database.models import S
# 登录处理
def signin(request):
    # 从 HTTP POST 请求中获取工号、密码参数
    teacherId = request.POST.get('gh')
    passWord = request.POST.get('password')
    try:
        # 根据学号从数据库学生表中找到相应的学生记录
        teacher = S.objects.get(xh=teacherId)
    except S.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'工号 为`{teacherId}`的教师不存在'
        }
    userName=teacher.xm
    # 使用 Django auth 库里面的方法校验用户名、密码
    user = authenticate(username=userName, password=passWord)
    # 如果能找到用户，并且密码正确
    if user is not None:
        if user.is_superuser:
            login(request, user)
            # 在session中存入用户类型
            request.session['usertype'] = 'teacher'
            return JsonResponse({'ret': 0})
        else:
            return JsonResponse({'ret': 1, 'msg': '请使用教师账户登录'})
    # 否则就是用户名、密码有误
    else:
        return JsonResponse({'ret': 1, 'msg': '账号或者密码错误'})

# 登出处理
def signout(request):
    # 使用登出方法
    logout(request)
    return JsonResponse({'ret': 0})