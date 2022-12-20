from django.shortcuts import render, redirect, get_object_or_404 #- нужно для перехода к странице в login
#добавление(импорт) формы для регистрации из джанго
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
#добавляем модель пользователя
from django.contrib.auth.models import User
#импорт ошибки из except строки
from django.db import IntegrityError
# импорт для перехода на новую страницу, при правильном введении имени и пароля и logout для выхода
#authenticate проверка имя пользователя и пароля при входе
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
#только зарегестрированные пользователи могут писать в форму
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request,'todo/home.html')
#создает функцию для страницы регистрации пользователя
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html',{'form':UserCreationForm()}) #отрисовывает страницу, и процедура сопоставления данных словоря со всеми данными пользователей
    #если пользователь не зарегестрирован
    else:
#сравниваем первый и второй пароль, если правильно то переходим к созданию нового пользователя
        if request.POST['password1'] == request.POST['password2']:
            try:
                #это всстроенная функция в джанго которая создает новых пользователей + передача данных имя/пароль
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                #сохраняем пользователя в базу данных
                user.save()
                #перехода на новую страницу, при правильном введении имени и пароля
                login(request,user)
                #перенаправление на страницу, после регистрации пользовател
                return redirect('currenttodos')
            # если имя уже существует, то выдаем текст + новое заполнение формы
            except IntegrityError:
                return render(request, 'todo/signupuser.html',{'form':UserCreationForm(),'error':'Это имя пользователя уже существует, зайдайте новое.'})
            except ValueError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Введите имя и пароль!'})
            #если пароли не совподает, то выдаем текст + новое заполнение формы,переменная error нужна только для отображения на html
        else:
            return render(request, 'todo/signupuser.html',{'form':UserCreationForm(),'error':'Не правильный пароль, попробуйте еще раз.'})
#функция для страницы входа пользователя
def loginuser(request):
    # если пользователь уже зарегестрирован, то метод гет
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})  # отрисовывает страницу, и процедура сопоставления данных ловоря со всеми данными пользователей
    #проверка регистрации пользователя на сайте
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # если имя или пароль не правильные, то выход на другую страницу
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(),'error':'Вы ввели неверный пароль или имя пользователя. Попробуйте ещё раз!'})
        #если удалость провисти аунтификацию то идет в ветку else
        else:
            # перехода на новую страницу, при правильном введении имени и пароля
            login(request, user)
            # перенаправление на страницу, после регистрации пользовател
            return redirect('currenttodos')
@login_required
#функция для страницы выхода пользователя
def logoutuser(request):
    #ФУНКЦИЯ БУДЕТ РАБОТАТЬ ТОЛЬКО ПРИ МЕТОДЕ POST
    if request.method == 'POST':
        #вызов функции logout
        logout(request)
        # переход на страницу после нажатия кнопки выход
        return redirect('home')

@login_required
#функция создания записей пользователем
def createtodo(request):
    if request.method == 'GET':
        #отображение формы записи для пользователя
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            #метод сохранения записи в БД и привязка к пользователю
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            #перенаправление на список записисей после сохранения текущей и её сохранение
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(),'error':'Неверная запись,превышено максимальное число символов!'})
@login_required
#отрисовка страницы после входа в систему
def currenttodos(request):
    #передаем данные из БД на страницу             #после завершения задачи, убирать задачу
    todos = Todo.objects.filter(user=request.user)
    return render(request,'todo/currenttodos.html',{'todos':todos})
@login_required
def completettodos(request):
    # передаем данные из БД на страницу             #после завершения задачи, НЕ убирать задачу
    todos = Todo.objects.filter(user=request.user, datevompleted__isnull=False).order_by('-datevompleted')#отображение списка от последнего к старому
    return render(request, 'todo/completettodos.html', {'todos': todos})
@login_required
#функция для открытия записей и их редактирования из страницы current
def viewstodo(request,todo_pk):
    #передает ключ из urls
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)#система сверяет ключ и владельца записиси
    if request.method == 'GET':
    #чтобы редактировать информацию из базы данных, передаем словарем form
        form = TodoForm(instance=todo)#параметр формы
        return render(request, 'todo/viewstodo.html', {'todo':todo, 'form':form})
    #после того как пользователь перешел в раздел редактирования,мы переходим в ветку else
    else:
        #если при редактировании будут допущены ошибки
        try:
            form = TodoForm(request.POST,instance=todo)
            form.save()
            #в случае успешного редактирования,перенаправление пользовател на currenttodos
            return redirect('currenttodos')
            #в случае ошибки отобразим
        except ValueError:
            return render(request, 'todo/viewstodo.html', {'todo': todo, 'form': form,'error':'Плохая информация:'})
@login_required
 #функция для завершения задач пользователем
def completetodo(request,todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) # система сверяет ключ и владельца записи
    if request.method == 'POST':
        #присвоение текущей даты и времени(заполнения поля в случая завершения задачи)
        todo.datevompleted = timezone.now() if todo.datevompleted == None else None
        todo.save()
        return redirect('currenttodos')



@login_required
    #функция удаления записи пользователя
def deletetodo(request,todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)  # система сверяет ключ и владельца записис
    if request.method == 'POST':
        todo.delete()
        return redirect('completettodos')







