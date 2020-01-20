from django.http import JsonResponse

from database.models import C,E,S
def listgrade(request):
    curStudent = S.objects.get(xh=request.session['member_id'])
    #curStudent = S.objects.get(xh='17123079')
    stucourse = E.objects.filter(xh=curStudent.xh)
    stucourse = list(stucourse)
    retlist=[]
    for i in stucourse:
        retlist.append({
            'kh':i.kh,
            'km':i.km,
            'xf':i.xf,
            'rkls':i.rkls,
            'zpcj':i.zpcj
        })
    #计算平均成绩
    totalgrade = 0
    count = 0
    for j in retlist:
        if j['zpcj']!="NULL":
            totalgrade += int(j['zpcj'])
            count += 1
    if count!=0:
        avgGrade = round(totalgrade/count,1)
    else:
        avgGrade = "NULL"
    return JsonResponse({'ret': 0, 'retlist': retlist,'avgGrade':avgGrade})