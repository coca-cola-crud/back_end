from django.http import JsonResponse
import json
from database.models import E,S,T,C,Y
from django.contrib.auth.models import User

def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理
    # GET请求 参数 在 request 对象的 GET属性中
    if request.method == 'GET':
        request.params = request.GET
    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST','DELETE','PUT']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'add_course':
        return addCourse(request)
    elif action == 'del_course':
        return delCourse(request)
    elif action == 'list_course':
        return listCourse(request)
    elif action == 'alter_info':
        return alterInfo(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})

#根据学院列出课表
def listCourse(request):
    request.params = json.loads(request.body)
    Yx = request.params['yx']
    courses = C.objects.filter(yx=Yx)
    #课程列表
    courses=list(courses)
    retlist=[]
    for i in courses:
        retlist.append({
           'kh':i.kh,
           'km':i.km,
            'xf':i.xf,
            'gh':i.gh,
            'yx':i.yx,
            'rkls':i.rkls,
            'sksj':i.sksj,
            'xkrs':i.xkrs,
            'xzrs':i.xzrs

        })
    #院系列表
    yxlist = []
    yx = Y.objects.values()
    yx = list(yx)
    for j in yx:
        yxlist.append(j['yxm'])

    return JsonResponse({'yxlist':yxlist,'retlist': retlist})

#开课
def addCourse(request):
    # 从请求消息中 获取要开课的信息
    info = request.params['data']
    teacherid=info['gh']
    try:
        # 根据 id 从数据库中找到相应的学生记录
        teacherinfo = T.objects.get(gh=info['gh'])
    except T.DoesNotExist:
        return JsonResponse({
            'ret': 1,
            'message': f'id 为`{teacherid}`的教师不存在'
        })
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    courseid=info['kh']
    flag=0
    qs = C.objects.values()
    Clist = list(qs)
    for i in Clist:
        if i['kh'] == courseid:
            flag=1
            break
    if flag!=1:
        addedcourse = C.objects.filter(gh=info['gh'])
        addedcourse = list(addedcourse)
        courses=C.objects.filter(gh=info['gh'])
        courses=list(courses)
        flag1 = 0
        for i in addedcourse:
            sametime = 0
            print(i.kh, i.sksj)
            # 判断上课时间是否有重合
            addedsksj = i.sksj.split(' ')
            addsksj = info['sksj'].split(' ')
            print(addsksj, addedsksj)
            for x in addedsksj:
                for y in addsksj:
                    xweek = x[0]
                    yweek = y[0]
                    xtime = x[1:].split('-')
                    ytime = y[1:].split('-')
                    if sametime == 0:
                        if xweek != yweek:
                            sametime = 0
                        elif int(xtime[1]) < int(ytime[0]) or int(ytime[1]) < int(xtime[0]):
                            sametime = 0
                        else:
                            sametime = 1
                            break
                    else:
                        break
            if sametime:
                flag1 = 1
                return JsonResponse({'ret': 1, 'message': '该教师该时间已开课，开课失败'})

        if flag1 == 0:
            C.objects.create(kh=info['kh'],
                             km=info['km'],
                             xf=info['xf'],
                             rkls=teacherinfo.xm,
                             yx=teacherinfo.yx,
                             gh=teacherinfo.gh,
                             sksj=info['sksj'],
                             xkrs=0,
                             xzrs=info['xzrs']
                            )
            return JsonResponse({'ret': 0, 'message':'添加成功'})
    else:
        return JsonResponse({'ret': 1, 'message':'该课号课程已开'})


#C表删除课程，E表中该教师开课记录同时删除，使用触发器
def delCourse(request):
    courseid = request.params['courseid']
    course = C.objects.get(kh=courseid)
    # delete 方法就将该记录从数据库中删除了
    course.delete()
    return JsonResponse({'ret': 0, 'msg': '删除成功'})

#修改课程信息,E表中也要改变
def alterInfo(request):

    courseid = request.params['courseid']
    newdata = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的课程记录
        course = C.objects.get(kh=courseid)
    except C.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{courseid}`的课程不存在'
        }

    if 'km' in newdata:
        print(newdata['km'])
        course.km = newdata['km']
    if 'xf' in newdata:
        course.xf = newdata['xf']
    if 'rkls' in newdata:
        course.xm = newdata['rkls']
    if 'gh' in newdata:
        course.gh = newdata['gh']
        teacher=T.objects.get(gh=newdata['gh'])
        course.yx=teacher.yx
    if 'sksj' in newdata:
        course.sksj = newdata['sksj']
    if 'zkrs' in newdata:
        course.zkrs = newdata['zkrs']
    if 'xkrs' in newdata:
        course.xkrs = newdata['xkrs']

    # 注意，一定要执行save才能将修改信息保存到数据库
    course.save()
