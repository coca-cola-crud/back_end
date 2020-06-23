from django.http import JsonResponse
import json
from database.models import C,E,S,T,X
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
    elif action == 'post_grade':
        return postgrade(request)
    elif action == 'grade_distribution':
        return gradeDistribution(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})

#列出该老师该学期开的课程
def listmycourse(request):
    curTeacher = T.objects.get(gh=request.session['member_id'])
    mycourse = C.objects.filter(gh=curTeacher.gh,xq=curTerm())
    mycourse = list(mycourse)
    retlist=[]
    for i in mycourse:
        retlist.append({
            'kh': i.kh,
            'km': i.km,

        })
    return JsonResponse({'ret': 0, 'retlist': retlist})

#列出选择某课的学生
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
            'zpcj': i.zpcj
        })
    return JsonResponse({'ret': 0, 'retlist': retlist})

#录入修改成绩
def postgrade(request):
    studentId = request.params['xh']
    courseId = request.params['kh']
    curTeacher = T.objects.get(gh=request.session['member_id'])
    student = E.objects.get(kh=courseId, xh=studentId,gh=curTeacher.gh)
    try:
        zpcj=float(request.params['zpcj'])
    except ValueError:
        return JsonResponse({'ret': 1, 'msg': '请输入数字'})

    if(zpcj<=100 and zpcj>=0):
        student.zpcj = request.params['zpcj']
        student.save()
        return JsonResponse({'ret': 0, 'msg': '成绩录入/修改成功'})
    else:
        return JsonResponse({'ret': 1, 'msg': '成绩录入/修改失败'})

#成绩分布
def gradeDistribution(request):
    courseId = request.params['kh']
    curTeacher = T.objects.get(gh=request.session['member_id'])
    # 找到选择该老师的课程的学生
    students = E.objects.filter(kh=courseId,gh=curTeacher.gh)
    students = list(students)
    retlist = [0,0,0,0,0,0,0,0,0,0,0]
    for i in students:
        if i.zpcj != "NULL":
            zpcj = float(i.zpcj)
            if zpcj < 60:
                retlist[0] += 1
            elif zpcj <= 63.9 and zpcj >= 60:
                retlist[1] += 1
            elif zpcj <= 65.9 and zpcj >= 64:
                retlist[2] += 1
            elif zpcj <= 67.9 and zpcj >= 66:
                retlist[3] += 1
            elif zpcj <= 71.9 and zpcj >= 68:
                retlist[4] += 1
            elif zpcj <= 74.9 and zpcj >= 72:
                retlist[5] += 1
            elif zpcj <= 77.9 and zpcj >= 75:
                retlist[6] += 1
            elif zpcj <= 81.9 and zpcj >= 78:
                retlist[7] += 1
            elif zpcj <= 84.9 and zpcj >= 82:
                retlist[8] += 1
            elif zpcj <= 89.9 and zpcj >= 85:
                retlist[9] += 1
            elif zpcj <= 100 and zpcj >= 90:
                retlist[10] += 1
    return JsonResponse({'retlist': retlist})
def curTerm():
    curterm = X.objects.get(status=1)
    return curterm.xq
