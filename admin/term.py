from django.http import JsonResponse
import json
from database.models import X
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
    if action == 'list_term':
        return listTerm(request)
    elif action == 'add_term':
        return addTerm(request)
    elif action == 'set_term':
        return setTerm(request)
    elif action == 'cur_term':
        return curTerm(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})

def listTerm(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = X.objects.values()
    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    print(qs)
    xqlist = list(qs)
    retlist=[]
    for i in xqlist:
        retlist.append(i['xq'])
    return JsonResponse({'ret': 0, 'retlist': retlist})

def addTerm(request):
    newterm = request.params['newterm']
    term = X.objects.values()
    term = list(term)
    flag=0
    for i in term:
        if newterm==i['xq']:
            flag=1
            break
    if flag==0:
        X.objects.create(xq=newterm)
        return JsonResponse({'ret':0,'message':'添加成功'})
    else:
        return JsonResponse({'ret':1,'message':'添加失败'})


def setTerm(request):
    curterm=request.params['curterm']
    X.objects.filter(status=1).update(status=0)
    term=X.objects.get(xq=curterm)
    term.status=1
    term.save()
    return JsonResponse({'ret': 0, 'message': '设置成功'})

def curTerm(request):
    curterm = X.objects.get(status=1)
    print(curterm.xq)
    return JsonResponse({'curterm': curterm.xq})