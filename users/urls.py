from django.urls import path
from users.views import register, login
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('logout', LogoutView.as_view(), name='logout')
]
