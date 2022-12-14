from django.forms import ModelForm
from .models import Todo


# форма для пользователя
class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']
