from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^users/$', views.index, name='index'),
    url(r'^users/(?P<id>[0-9]+)', views.show, name='show'),
    url(r'^users/add', views.add, name='add'),
    url(r'^users/update/(?P<id>[0-9]+)', views.update, name='update'),
    url(r'^users/delete/(?P<id>[0-9]+)', views.delete, name='delete'),

    url(r'^presents/$', views.todayPresence, name='todayPresence'),
    url(r'^presents/enter/(?P<id>[0-9]+)', views.addEnter, name='enter'),
    url(r'^presents/out/(?P<id>[0-9]+)', views.addOut, name='out'),

    url(r'^payments/$', views.paymentList, name='paymentList'),
    url(r'^payments/add/(?P<id>[0-9]+)', views.addPayment, name='addPayment'),

    url(r'^user-diagram/$', views.userDiagram, name='userDiagram'),
]