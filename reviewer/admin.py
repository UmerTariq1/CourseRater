from django.contrib import admin

# Register your models here.
from .models import CourseItem, Rating
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(CourseItem)
admin.site.register(Rating)
admin.site.register(CustomUser, UserAdmin)