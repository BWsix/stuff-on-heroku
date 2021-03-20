from django.contrib import admin

from .models import User, LunchOrder, LunchMenu

admin.site.register(User)
admin.site.register(LunchMenu)
admin.site.register(LunchOrder)
