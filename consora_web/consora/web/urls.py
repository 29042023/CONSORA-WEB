from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('panel/', views.dashboard, name='dashboard'),
    path('panel/asistentes/', views.asistentes, name='asistentes'),
    path('panel/chat/', views.chat, name='chat'),
]