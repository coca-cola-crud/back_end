from django.http import JsonResponse

from database.models import C,E,S,X
def listgrade(request):
    curStudent = S.objects.get(xh=request.session['member_id'])
    #curStudent = S.objects.get(xh='17123079')
    stucourse = E.objects.filter(xh=curStudent.xh,xq=curTerm())
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
    avgGrade=countGrade(stucourse)
    # totalgrade = 0
    # count = 0
    # for j in retlist:
    #     if j['zpcj']!="NULL":
    #         totalgrade += int(j['zpcj'])
    #         count += 1
    # if count!=0:
    #     avgGrade = round(totalgrade/count,1)
    # else:
    #     avgGrade = "NULL"
    return JsonResponse({'ret': 0, 'retlist': retlist,'avgGrade':avgGrade})

def curTerm():
    curterm = X.objects.get(status=1)
    return curterm.xq

def countGrade(stucourse):
    totalgrade = 0
    count = 0
    for j in stucourse:
        if j.zpcj!= "NULL":
            totalgrade += int(j.zpcj)
            count += 1
    if count != 0:
        avgGrade = round(totalgrade / count, 1)
    else:
        avgGrade = 0
    return avgGrade

def gradeTend(request):
    curStudent = S.objects.get(xh=request.session['member_id'])
    #curStudent = S.objects.get(xh='17123079')
    retlist=[]
    term = X.objects.values()
    term = list(term)
    for i in term:
        stucourse = E.objects.filter(xh=curStudent.xh,xq=i["xq"])
        stucourse = list(stucourse)
        avgGrade = countGrade(stucourse)
        retlist.append(avgGrade)
    print(retlist)
    return JsonResponse({'retlist': retlist})
