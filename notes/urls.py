from django.urls import path
from . import views

urlpatterns=[
    path('register/',views.register,name="register"),
    path('login/',views.login_view,name="login"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('logout/',views.logout_view),
    path('todo/', views.todo, name="todo"),
    path('update_todo/<int:pk>/', views.update_todo, name="update_todo"),
    path('delete_todo/<int:pk>/', views.delete_todo, name="delete_todo"),
]
