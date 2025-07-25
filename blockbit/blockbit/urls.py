from django.contrib import admin
from django.urls import path, include
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('accounts/', include('django.contrib.auth.urls')),  # Built-in auth URLs
    path('accounts/login/', views.user_login, name="login"),  # Built-in auth URLs
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/profile/', views.profile, name='profile'),
    path('', views.home, name='home'),  # Update with your home view
]