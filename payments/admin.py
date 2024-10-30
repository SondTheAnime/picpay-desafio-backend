from django.contrib import admin
from .models import Transaction, CeleryTask

@admin.register(CeleryTask)
class CeleryTaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'task_name', 'status', 'date_done')
    list_filter = ('status', 'task_name')
    search_fields = ('task_id', 'task_name')
    readonly_fields = ('task_id', 'task_name', 'status', 'result', 'date_done')
    ordering = ('-date_done',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Transaction)