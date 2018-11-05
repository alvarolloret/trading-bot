from django.conf.urls import url
from django.urls import path
from trader_app import views

# SET THE NAMESPACE!
app_name = 'trader_app'

urlpatterns = [
    # path("backtest/",views.backtest,name='backtest'),
    url(r'^backtest/',views.backtest,name='backtest'),
    url(r'^livetesting/',views.livetesting,name='livetesting'),
    url(r'^outputResult/',views.outputResult,name='outputResult'),
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
]
