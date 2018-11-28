from django.contrib import admin
from trader_app.models import UserProfileInfo, User, CandleStick, Strategy

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(CandleStick)
admin.site.register(Strategy)
