from django.contrib import admin
from trader_app.models import UserProfileInfo, User, CandleStick_4H_ETH_USDT

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(CandleStick_4H_ETH_USDT)
