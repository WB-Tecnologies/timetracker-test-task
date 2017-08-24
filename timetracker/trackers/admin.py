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
    list_display = ['title', 'date_added', 'TYPE_CHOICES', 'owner']
    list_filter = ('TYPE_CHOICES', )
    inlines = [TimeSpendInLine]

    class Meta:
        verbose_name_plural = "Activities"

admin.site.register(Activity, ActivityAdmin)
admin.site.register(TimeSpend, TimeSpendAdmin)
