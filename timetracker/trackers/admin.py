from django.contrib import admin

from .models import Activity, TimeSpend


class TimeSpendAdmin(admin.ModelAdmin):
    list_display = ['activity', 'date']


class TimeSpendInLine(admin.TabularInline):
    model = TimeSpend
    show_change_link = True
    extra = 1


class ActivityAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'date_added', 'type', 'owner']
    list_filter = ('type', )
    inlines = [TimeSpendInLine]

    class Meta:
        verbose_name_plural = "Activities"

admin.site.register(Activity, ActivityAdmin)
admin.site.register(TimeSpend, TimeSpendAdmin)
