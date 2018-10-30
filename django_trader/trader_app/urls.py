from django.conf.urls import url
from trader_app import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^$',views.index,name='outputResult'),
]
