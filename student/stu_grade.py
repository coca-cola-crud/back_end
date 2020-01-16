from django.http import JsonResponse

from database.models import C,E,S
def listgrade(request):
    curStudent = S.objects.get(xh=request.session['member_id'])
    #curStudent = S.objects.get(xh='17123101')
    stucourse = E.objects.filter(xh=curStudent.xh)
    stucourse = list(stucourse)
    retlist=[]
    for i in stucourse:
        retlist.append({
            'xh':i.kh,
            'km':i.km,
            'xf':i.xf,
            'rkls':i.rkls,
            'gh':i.gh,
            'zpcj':i.zpcj
        })
    return JsonResponse({'ret': 0, 'retlist': retlist})