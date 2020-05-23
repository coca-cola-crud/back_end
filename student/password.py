from django.http import JsonResponse
from django.db import connection
from django.contrib.auth.models import User
from database.models import S
import json
def alterpassword(request):
    print(request.session['member_id'])
    request.params = json.loads(request.body)
    newpassword = request.params['newpassword']
    oldpassword = request.params['oldpassword']
    student = S.objects.get(xh=request.session['member_id'])
    user = User.objects.get(username=student.xh)
    if user.check_password(oldpassword):
        user.set_password(newpassword)
        user.save()
        return JsonResponse({'ret': 0, 'msg': '密码修改成功'})
    else:
        return JsonResponse({'ret':1,'msg':'密码错误'})
