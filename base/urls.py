from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('topic/', views.topic, name="topic"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('login/', views.loginpage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutuser, name="logout"),
    path('user-profile/<str:pk>/', views.userprofile, name="user"),
    path('update-user/', views.updateuser, name="update-user"),
    path('about/', views.about, name="about"),
]
