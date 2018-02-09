from django.shortcuts import render
from django.http import HttpResponse
from .models import *


# Create your views here.


def register(request):
    """注册逻辑
    127.0.0.1:8000/users/register/ ../static/css/reset.css
    127.0.0.1:8000/users/static/css/reset.css
    127.0.0.1:8000/users/register ../static/css/reset.css #最后一个/ zuo是当前文件夹
    127.0.0.1:8000/static/css/reset.css

    """

    if request.method == "GET":
        return render(request, "register.html")  # 天天生鲜里不再使用应用去区分模板
    elif request.method == "POST":

        return HttpResponse("测试")
