from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created_at', 'updated_at')


# Register your models here.
admin.site.register(Task, TaskAdmin)