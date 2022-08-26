from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Event


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'name',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Event)
