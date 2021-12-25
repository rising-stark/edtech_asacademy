from django.contrib import admin
from django.urls import path
from src import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('register/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),

    # Post requests
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
]
