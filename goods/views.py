from django.shortcuts import render

# Create your views here.
from django.views.generic import View


# 主页无需登陆即可访问添加购物车
class IndexView(View):

    def get(self, request):
        """查询主页商品数据"""
        return render(request, 'index.html')

    def post(self, request):
        pass
