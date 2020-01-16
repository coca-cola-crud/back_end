from django.http import JsonResponse

from database.models import T

def list_info(request):
        print(request.session['member_id'])
        teacher = T.objects.get(gh=request.session['member_id'])
        print(teacher.xm)
        return JsonResponse({'xm':teacher.xm,'gh': teacher.gh,'xb': teacher.xb,'xl': teacher.xl,'yx': teacher.yx})