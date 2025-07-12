from django.urls import path
from profiles.views import profile_detail

urlpatterns = [
    path('profile', profile_detail, name='profile'),
]
