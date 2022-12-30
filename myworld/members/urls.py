from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.login,name='login'),
    path('login/check/',views.check,name='check'), 
    path('add/',views.add,name='add'),
    path('add/addrecord/',views.addrecord,name='addrecord'),
    #第二步，指出哪个路径要调用什么view，同时要指明参数类型
    path('adminpage/delete/<int:id>', views.delete, name='delete'),
    path('update/<int:id>',views.update,name='update'),
    path('update/updaterecord/<int:id>',views.updaterecord,name='updaterecord'),
    path('infopage/<int:id>',views.infopage,name='infopage'),
    path('searchres/',views.searches,name='searches'),
    path('adminpage/',views.adminpage,name='adminpage'),
    path('faultpage/',views.faultpage,name='faultpage'),
]