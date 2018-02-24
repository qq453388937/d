# -*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from users.views import Address


class MyLoginBaseViewMixin(object):
    """
    重写asview() 方法 Address.as_view()找到就会执行
    哪个类视图需要登陆验证继承MyLoginView即可

    MyLoginBaseView 和 View耦合性太强 ，解耦就不能直接继承View 因为还有 TemplateView
    """
    # 登陆校验装饰器
    from django.contrib.auth.decorators import login_required

    @classmethod
    def as_view(cls, **initkwargs):
        """
        经典类class A1():多继承属性搜索顺序: 先深入继承树左侧，再返回，开始找右侧;
        新式类class A1(object):多继承属性搜索顺序: 先水平搜索，然后再向上移动
        super(B, self).func的调用并不是一定用于调用当前类的父类的func函数
        Python的多继承类是通过mro的方式来保证各个父类的函数被逐一调用，
        而且保证每个父类函数只调用一次（如果每个类都使用super）；
        """
        # view = super(SpecialView, self).as_view(cls, **initkwargs)
        # view = super(MyLoginBaseView, cls).as_view(**initkwargs)

        view = super(MyLoginBaseViewMixin, cls).as_view(**initkwargs)
        """
        因为调用的是Address.as_view(),所以这里的super().as_view(**initkwargs) ==> Address.super().as_view()
        而Address有两个父类第一个是MyLoginBaseView，第二个是View,
        因为进入到MyLoginBaseView 的as_view() ，又调用了Address.super().as_view()所以不会再找一次，
        继续找，找到平行父级View的as_view() 方法,如果找不到再找object ,object 没有才会报错！

        """
        # view = super().as_view(**initkwargs)  # 新式类写法横向查找
        return login_required(view)  # 返回带登陆校验的结果

        """ 如果 return  view就是直接return view 不带权限校验的"""

# 耦合度太强
# class MyLoginBaseView(TemplateView):
#     @classmethod
#     def as_view(cls, **initkwargs):
#         view = super().as_view(**initkwargs)
#         return login_required(view)
