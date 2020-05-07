from django.http import JsonResponse
from django.db import connection

from database.models import S

def list_info(request):
        Xh = request.session['member_id']
        cursor = connection.cursor()
        cursor.execute("select * from S where xh=%s", [Xh])
        student = cursor.fetchall()
        return JsonResponse({'xm':student[0][1],
                             'xh': student[0][0],
                             'nl':student[0][2],
                             'xb': student[0][3],
                             'yx': student[0][4]})
