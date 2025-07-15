from django.urls import path
from profiles.views import profile_detail, ProfileCreateView, ProfileUpdateView, CareerItemCreateView,CareerItemUpdateView, CareerItemDeleteView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(profile_detail), name='profile'),
    path('create', login_required(ProfileCreateView.as_view()), name='profile_create'),
    path('edit', login_required(ProfileUpdateView.as_view()), name='profile_update'),
    path('<str:item_type>/create', login_required(CareerItemCreateView.as_view()), name='career_item_create'),
    path('<str:item_type>/edit/<int:pk>', login_required(CareerItemUpdateView.as_view()), name='career_item_edit'),
    path('<str:item_type>/delete/<int:pk>', login_required(CareerItemDeleteView.as_view()), name='career_item_delete'),
]
