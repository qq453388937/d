from django.shortcuts import render

# Create your views here.
from django.views.generic import View


class IndexView(View):
    def get(self, request):
        """查询主页商品数据"""
        pass
        return render(request, 'index.html')

    def post(self):
        pass
