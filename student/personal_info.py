from django.http import JsonResponse
import json


from database.models import S

def list_info(request):
        print(request.session['member_id'])
        student = S.objects.get(xh=request.session['member_id'])
        print(student.xm)
        # 返回一个 QuerySet 对象 ，包含所有的表记录

        # 将 QuerySet 对象 转化为 list 类型
        # 否则不能 被 转化为 JSON 字符串
        return JsonResponse({'xm':student.xm,'xh': student.xh,'nl':student.nl,'xb': student.xb,'yx': student.yx})