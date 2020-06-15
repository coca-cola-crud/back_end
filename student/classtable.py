from django.http import JsonResponse
from django.db import connection
from django.contrib.auth.models import User
from database.models import S,E
import json
def classtable(request):
    student = S.objects.get(xh=request.session['member_id'])
    selectedcourse=E.objects.filter(xh=student.xh)
    selectedcourse=list(selectedcourse)
    print(selectedcourse)
    Mon=['','','','','','','','','','','','','']
    Tue=['','','','','','','','','','','','','']
    Wes=['','','','','','','','','','','','','']
    Thu=['','','','','','','','','','','','','']
    Fri=['','','','','','','','','','','','','']

    lessons=[ '08:00-09:00',
              '09:00-10:00',
              '10:00-11:00',
              '11:00-12:00',
              '13:00-14:00',
              '14:00-15:00',
              '15:00-16:00',
              '16:00-17:00',
              '17:00-18:00',
              '18:00-19:00',
              "19:00-20:00",
              "20:00-21:00",
              "21:00-22:00" ]

    for i in selectedcourse:
        print(i)
        sksj=i.sksj.split(" ")
        for j in sksj:#j格式 四3-5
            if j[0] == "一":
                time=j[1:].split('-')
                start=int(time[0])
                end=int(time[1])
                while start<=end:
                    Mon[start]=i.km
                    start+=1
            elif j[0] == "二":
                time=j[1:].split('-')
                start=int(time[0])
                end=int(time[1])
                while start<=end:
                    Tue[start-1]=i.km
                    start+=1
            elif j[0] == "三":
                time = j[1:].split('-')
                start = int(time[0])
                end = int(time[1])
                while start <= end:
                    Wes[start-1]=i.km
                    start += 1
            elif j[0] == "四":
                time = j[1:].split('-')
                start = int(time[0])
                end = int(time[1])
                while start <= end:
                    Thu[start-1]=i.km
                    start += 1
            elif j[0] == "五":
                time = j[1:].split('-')
                start = int(time[0])
                end = int(time[1])
                while start <= end:
                    Fri[start-1]=i.km
                    start += 1

    return JsonResponse({'lessons':lessons,'courses': [
        Mon, Tue, Wes, Thu, Fri
    ]})



