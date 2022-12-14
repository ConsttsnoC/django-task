from django.contrib import admin
#импорт моделей из моделс для отображения их в админке
from .models import Todo


#чтобы показывала дату создания
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Todo, TodoAdmin)
