"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#ипорт файла из приложения
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

#путь к странице регистрации пользователя
    path('signup/', views.signupuser, name='signupuser'),
#страница для входа пользователя
    path('login/', views.loginuser, name='loginuser'),
#страница для ВЫХОДА пользователя
    path('logout/', views.logoutuser, name='logoutuser'),
#страница пользователя
    path('', views.home, name='home'),
    # создание страницы для записей пользователей
    path('create/', views.createtodo, name='createtodo'),
    #после выхода,идет переход на эту страницу
    path('current/', views.currenttodos, name='currenttodos'),
    #для открытия записи из current
    path('todo/<int:todo_pk>', views.viewstodo, name='viewstodo'),
    #url для завершения задач
    path('todo/<int:todo_pk>/complete', views.completetodo, name='completetodo'),
    #url удаления записи "дела"
    path('todo/<int:todo_pk>/delete', views.deletetodo, name='deletetodo'),
    #отображения задач для пользователя
    path('completet/', views.completettodos, name='completettodos'),
]
