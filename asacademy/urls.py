from django.contrib import admin
from django.urls import path
from src import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('home/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('booknow/', views.booknow, name='booknow'),
    path('book/', views.booknow, name='booknow'),
    path('about/', views.about, name='about'),
    path('planspricing/', views.planspricing, name='planspricing'),
    path('contact/', views.contact, name='contact'),
    path('addchild/', views.addchild, name='addchild'),
    path('stripe_payment/', views.stripe_payment, name='stripe_payment'),
    path('purchase/', views.purchase, name='purchase'),

    # Post requests
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('contact', views.contact, name='contact'),
    path('addchild', views.addchild, name='addchild'),
    path('stripe_payment', views.stripe_payment, name='stripe_payment'),
]
