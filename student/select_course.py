from django.http import JsonResponse
import json
from database.models import C,E,S,X
def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理
    # GET请求 参数 在 request 对象的 GET属性中
    if request.method == 'GET':
        request.params = request.GET
    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST','DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_course':
        return listcourse(request)
    elif action == 'list_selected_course':
        return listselectedcourse(request)
    elif action == 'select_course':
        return selectcourse(request)
    elif action == 'del_course':
        return deletecourse(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})

#列出当前学期可选课程，开课表
def listcourse(request):
    print(curTerm())
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = C.objects.filter(xq=curTerm())
    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    #print(qs)
    courselist = list(qs)
   # print(retlist)
    for i in courselist:
        courseid=i.kh
        course = C.objects.get(kh=courseid)
        course.xkrs = xknum(courseid)
        course.save()
    retlist=[]
    for i in courselist:
        retlist.append({
            'rkls':i.rkls,
            'gh':i.gh,
            'sksj':i.sksj,
            'xzrs':i.xzrs,
            'xkrs':i.xkrs,
            'km':i.km,
            'kh':i.kh,
            'xf':i.xf,
            'yx':i.yx
        })
        print(retlist)
    return JsonResponse({'ret': 0, 'retcourselist': retlist})

#列出已选课程
def listselectedcourse(request):
    # 获得当前学生信息
    curStudent = S.objects.get(xh=request.session['member_id'])
    #返回该学生的选课记录
    Eqs = E.objects.filter(xh=curStudent.xh,xq=curTerm())
    Cqs = C.objects.values()
    # 将 QuerySet 对象 转化为 list 类型
    Elist = list(Eqs)
    Clist = list(Cqs)
    retlist = []
    #在C表中找到该学生选过的课程添加到retlist
    for i in Elist:
        for j in Clist:
            if j['kh'] == i.kh and j['gh'] == i.gh:
                retlist.append(j)
    return JsonResponse({'ret': 0, 'retlist': retlist})


#选课
def selectcourse(request):
    #获取请求信息里的课程号
    select_kh = request.params['selectkh']
    #根据课程号在C表中获得课程信息
    try:
        selectinfo = C.objects.get(kh=select_kh)
    except C.DoesNotExist:
        return JsonResponse({
                'ret': 1,
                'msg': f'没有课号为{select_kh}的课程'
        })
    # 判断是否该课程选课人数是否已满
    if selectinfo.xkrs < selectinfo.xzrs:
        curStudent = S.objects.get(xh=request.session['member_id'])
        Id = curStudent.xh + selectinfo.kh
        selectedcourse = E.objects.filter(xh=curStudent.xh,xq=curTerm())
        selectedcourse = list(selectedcourse)

        flag = 0
        for i in selectedcourse:
            sametime = 0
            print(i.kh, i.sksj)
            # 判断上课时间是否有重合
            selectedsksj = i.sksj.split(' ')
            selectsksj = selectinfo.sksj.split(' ')
            print(selectsksj, selectedsksj)
            for x in selectedsksj:
                for y in selectsksj:
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

            if i.kh == selectinfo.kh:
                flag = 1
                return JsonResponse({'ret': 1, 'msg': f'{i.km}已选，选课失败'})
            elif sametime:
                flag = 1
                return JsonResponse({'ret': 1, 'msg': '时间冲突，选课失败'})

        if flag == 0:
            E.objects.create(xh=curStudent.xh,
                             kh=selectinfo.kh,
                             id=Id,
                             km=selectinfo.km,
                             xf=selectinfo.xf,
                             sksj=selectinfo.sksj,
                             rkls=selectinfo.rkls,
                             gh=selectinfo.gh,
                             zpcj="NULL",
                             xq=curTerm())
            courseid = selectinfo.kh
            course = C.objects.get(kh=courseid)
            course.xkrs = xknum(courseid)
            course.save()
        return JsonResponse({'ret': 0, 'msg': '选课成功'})

    else:
        return JsonResponse({
            'ret': 1,
            'msg': '课程人数已满，选课失败'
        })


#删除一条选课记录
def deletecourse(request):
    curStudent = S.objects.get(xh=request.session['member_id'])
    courseId = request.params['courseid']
    try:
        # 根据 courseId，xh 从E表中找到相应的选课记录
        course = E.objects.get(kh=courseId,xh=curStudent.xh)
    except E.DoesNotExist:
        return JsonResponse({
                'ret': 1,
                'msg': f'未选课号为{courseId}的课程'
        })
    # delete 方法就将该记录从数据库中删除了
    course.delete()
    course = C.objects.get(kh=courseId)
    course.xkrs = xknum(courseId)
    course.save()
    return JsonResponse({'ret': 0,'msg':'删除成功'})


def xknum(courseid):
    qs=E.objects.filter(kh=courseid)
    count = 0
    qs=list(qs)
    for i in qs:
        count+=1
    print(count)
    return count

def curTerm():
    curterm = X.objects.get(status=1)
    return curterm.xq
