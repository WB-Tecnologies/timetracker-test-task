from django.contrib import admin
from django.contrib.auth.models import User

from trackers.models import Activity


class ActivityInLine(admin.TabularInline):
    model = Activity
    show_change_link = True
    extra = 1
    readonly_fields = ('title', 'type', )


class UserAdmin(admin.ModelAdmin):
    inlines = [
        ActivityInLine
    ]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

