from django.http import JsonResponse
import json
from database.models import C,E,S
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
    if action == 'list_students':
        return listStudents(request)
    elif action == 'add_student':
        return addStudent(request)
    elif action == 'del_student':
        return delStudent(request)
    elif action == 'alter_info':
        return alterInfo(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})

#列出所有学生的信息
def listStudents(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = S.objects.values()
    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    print(qs)
    retlist = list(qs)
    for i in retlist:
        i.popitem()
    return JsonResponse({'ret': 0, 'retstudentlist': retlist})

#添加学生
def addStudent(request):
    info = request.params['data']
    flag = 0
    qs = S.objects.values()
    retlist = list(qs)
    for i in retlist:
        if i['xh'] == info['xh']:
            flag = 1
            break
    if flag!=0:
        # 从请求消息中 获取要添加学生的信息
        # 并且插入到数据库中
        # 返回值 就是对应插入记录的对象
        record = S.objects.create(xh=info['xh'] ,
                                xm=info['xm'] ,
                                nl=info['nl'],
                                xb=info['xb'],
                                yx=info['yx'],
                                sjhm=info['sjhm'],
                                mm=info['mm'])
        User.objects.create_user(username=record.xh, password=record.mm)
        return JsonResponse({'ret': 0, 'message':'添加成功'})
    else:
        return JsonResponse({'ret': 1, 'message': '学号重复'})


#删除学生，选课表中该学生选课记录同时删除，使用触发器？
def delStudent(request):
    curStudent = S.objects.get(xh=request.session['member_id'])
    courseId = request.params['courseid']
    try:
        # 根据 courseId，xh 从E表中找到相应的选课记录
        course = E.objects.get(kh=courseId, xh=curStudent.xh)
    except E.DoesNotExist:
        return JsonResponse({
            'ret': 1,
            'msg': f'未选课号为{courseId}的课程'
        })
    # delete 方法就将该记录从数据库中删除了
    course.delete()
    return JsonResponse({'ret': 0, 'msg': '删除成功'})


#修改信息
def alterInfo(request):
    # 从请求消息中 获取修改学生的信息
    # 找到该学生，并且进行修改操作

    studentid = request.params['studentid']
    newdata = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的学生记录
        student = S.objects.get(xh=studentid)
    except S.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{studentid}`的学生不存在'
        }

    if 'age' in newdata:
        print(newdata['age'])
        student.nl = newdata['age']
    if 'phone' in newdata:
        student.sjhm = newdata['phone']
    if 'name' in newdata:
        student.xm = newdata['name']
    if 'sex' in newdata:
        student.xb = newdata['sex']
    if 'major' in newdata:
        student.yx = newdata['major']

    # 注意，一定要执行save才能将修改信息保存到数据库

    student.save()

    return JsonResponse({'ret': 0})


