"""django_trader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from trader_app import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    # path("",views.index,name='index'),
    # path("<trader_app>/",include('trader_app.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^trader_app/',include('trader_app.urls')),
    url(r'^logout/$', views.user_logout, name='logout'),
]
