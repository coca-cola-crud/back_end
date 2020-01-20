from django.http import JsonResponse
import json
from database.models import C,E,S,T
def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理
    # GET请求 参数 在 request 对象的 GET属性中
    if request.method == 'GET':
        request.params = request.GET
    # POST请求 参数 从 request 对象的 body 属性中获取
    elif request.method == 'POST':
        # 根据接口，POST请求的消息体是 json格式
        request.params = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_my_course':
        return listmycourse(request)
    elif action == 'list_students':
        return liststudents(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})

#列出该老师开的课程
def listmycourse(request):
    curTeacher = T.objects.get(gh=request.session['member_id'])
    mycourse = C.objects.filter(gh=curTeacher.gh)
    mycourse = list(mycourse)
    retlist=[]
    for i in mycourse:
        retlist.append({
            'kh': i.kh,
            'km': i.km,
        })
    return JsonResponse({'ret': 0, 'retlist': retlist})

def liststudents(request):
    courseId = request.params['kh']
    curTeacher = T.objects.get(gh=request.session['member_id'])
    #找到选择该老师的课程的学生
    students = E.objects.filter(kh=courseId,gh=curTeacher.gh)
    students = list(students)
    retlist = []
    for i in students:
        stuname = S.objects.get(xh=i.xh).xm
        retlist.append({
            'xh': i.xh,
            'xm': stuname,
        })
    return JsonResponse({'ret': 0, 'retlist': retlist})
