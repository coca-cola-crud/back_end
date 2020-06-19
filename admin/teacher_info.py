from django.http import JsonResponse
import json
from database.models import E,S,T
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
    if action == 'list_teachers':
        return listTeachers(request)
    elif action == 'add_teacher':
        return addTeacher(request)
    elif action == 'del_teacher':
        return delTeacher(request)
    elif action == 'alter_info':
        return alterInfo(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})

#列出所有教师的信息
def listTeachers(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = T.objects.values()
    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    print(qs)
    retlist = list(qs)
    for i in retlist:
        i.popitem()#不返回密码
    return JsonResponse({'ret': 0, 'retteacherlist': retlist})

#添加
def addTeacher(request):
    info = request.params['data']

    # 从请求消息中 获取要添加学生的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    flag=0
    qs = T.objects.values()
    retlist = list(qs)
    for i in retlist:
        if i['gh'] == info['gh']:
            flag=1
            break
    if flag!=1:
        record = T.objects.create(gh=info['gh'] ,
                                xm=info['xm'] ,
                                xl=info['xl'],
                                xb=info['xb'],
                                yx=info['yx'],
                                sjhm=info['sjhm'],
                                mm=info['mm'])
        User.objects.create_user(username=record.gh, password=record.mm)
        return JsonResponse({'ret': 0, 'message':'添加成功'})
    else:
        return JsonResponse({'ret': 1, 'message':'工号重复'})


#删除教师，开课表中该教师开课记录同时删除，使用触发器？
def delTeacher(request):
    teacherid = request.params['teacherid']
    teacher = T.objects.get(gh=teacherid)
    # delete 方法就将该记录从数据库中删除了
    teacher.delete()
    User.objects.get(username=teacherid).delete()
    return JsonResponse({'ret': 0, 'msg': '删除成功'})


#修改信息
def alterInfo(request):
    # 从请求消息中 获取修改教师的信息
    # 找到该教师，并且进行修改操作

    teacherid = request.params['teacherid']
    newdata = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的学生记录
        teacher = T.objects.get(gh=teacherid)
    except S.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{teacherid}`的学生不存在'
        }

    if 'xl' in newdata:
        print(newdata['xl'])
        teacher.xl = newdata['xl']
    if 'sjhm' in newdata:
        teacher.sjhm = newdata['sjhm']
    if 'xm' in newdata:
        teacher.xm = newdata['xm']
    if 'xb' in newdata:
        teacher.xb = newdata['xb']
    if 'yx' in newdata:
        teacher.yx = newdata['yx']

    # 注意，一定要执行save才能将修改信息保存到数据库

    teacher.save()

    return JsonResponse({'ret': 0})


