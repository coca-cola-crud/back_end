from django.http import JsonResponse
from django.db import connection

from database.models import A


def list_info(request):
    admin = A.objects.get(gh=request.session['member_id'])
    return JsonResponse({'xm': admin.xm, 'gh': admin.gh, 'xb': admin.xb, 'sjhm': admin.sjhm, 'yxdz': admin.yxdz})
