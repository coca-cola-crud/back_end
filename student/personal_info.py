from django.http import JsonResponse
import json


from database.models import S

def list_info(request):
        print(request.session['member_id'])
        student = S.objects.get(xh=request.session['member_id'])
        print(student.xm)
        return JsonResponse({'xm':student.xm,'xh': student.xh,'nl':student.nl,'xb': student.xb,'yx': student.yx})