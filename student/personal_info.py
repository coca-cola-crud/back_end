from django.http import JsonResponse
from django.db import connection

from database.models import S

def list_info(request):
    print(request.session['member_id'])
    student = S.objects.get(xh=request.session['member_id'])
    # print(teacher.xm)
    return JsonResponse({'xm': student.xm, 'xh': student.xh, 'xb': student.xb, 'nl': student.nl, 'yx': student.yx,'sjhm':student.sjhm})
