from django.http import JsonResponse
import json
from database.models import C,E,Y
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
    if action == 'list_yx':
        return listYx(request)
    elif action == 'add_yx':
        return addYx(request)
    elif action == 'del_yx':
        return delYx(request)
    elif action == 'alter_info':
        return alterInfo(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})

#列出所有院系的信息
def listYx(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Y.objects.values()
    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    print(qs)
    retlist = list(qs)
    return JsonResponse({'ret': 0, 'retyxlist': retlist})

#添加院系
def addYx(request):
    info = request.params['data']
    flag = 0
    qs = Y.objects.values()
    retlist = list(qs)
    for i in retlist:
        if i['yxh'] == info['yxh']:
            flag = 1
            break
    if flag==0:
        # 从请求消息中 获取要添加院系的信息
        # 并且插入到数据库中
        # 返回值 就是对应插入记录的对象
        record = Y.objects.create(yxh=info['yxh'] ,
                                yxm=info['yxm'] ,
                                dz=info['dz'],
                                dh=info['dh'])

        return JsonResponse({'ret': 0, 'message':'添加成功'})
    else:
        return JsonResponse({'ret': 1, 'message': '院系号重复'})


#删除院系
def delYx(request):
    yxid = request.params['yxid']
    yx = Y.objects.get(yxh=yxid)

    # delete 方法就将该记录从数据库中删除了
    yx.delete()
    return JsonResponse({'ret': 0, 'msg': '删除成功'})


#修改信息
def alterInfo(request):
    # 从请求消息中 获取修改学生的信息
    # 找到该学生，并且进行修改操作

    yxid = request.params['yxid']
    newdata = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的学生记录
        yx = Y.objects.get(yxh=yxid)
    except Y.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{yxid}`的学生不存在'
        }

    if 'yxm' in newdata:
        print(newdata['yxm'])
        yx.yxm = newdata['yxm']
    if 'dz' in newdata:
        yx.dz = newdata['dz']
    if 'dh' in newdata:
        yx.dh = newdata['dh']

    # 注意，一定要执行save才能将修改信息保存到数据库
    yx.save()
    return JsonResponse({'ret': 0})


