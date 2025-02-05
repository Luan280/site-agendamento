from django.contrib import admin
from .models import User, Service, Calendar, Appointment, Payment
from site_agendamento import models

admin.site.register(User)
admin.site.register(Service)

admin.site.register(Appointment)
admin.site.register(Payment)


@admin.register(models.Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = 'date', 'time', 'is_available',
    list_per_page = 14
    list_max_show_all = 200
    list_editable = 'is_available',
    ordering = 'id',
    search_fields = 'date',
    list_filter = 'date',
