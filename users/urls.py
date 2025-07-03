from django.urls import path
from users.views import register
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('register', register, name='register'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout')
]
