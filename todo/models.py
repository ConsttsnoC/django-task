from django.db import models
#нужно чтобы привязать конкретного пользователя
from django.contrib.auth.models import User


#модель необходима для записи в базу данных
class Todo(models.Model):
    #атрибуты в админке
    #название "дела"
    title = models.TextField(null=True, blank=True)
    #описание "дела"
    memo = models.TextField(null=True, blank=True)
    #дата и время создание записи(создаваемый автоматически)
    created = models.DateTimeField(auto_now_add=True)
    #отметка о времени о выполнение дела
    datevompleted = models.DateTimeField(null=True, blank=True)
    #для галочки(отметки о выполнении)
    important = models.BooleanField(default=False)
    #создание модели привязки пользователя и модели, с помощью внешнего ключа (id+поле)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #функция отображения названий записей в списке в админке
    def __str__(self):
        return self.title