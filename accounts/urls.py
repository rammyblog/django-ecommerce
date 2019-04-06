from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegister, name='register'),
    path('profile/add', views.newUserProfile, name='user_profile'),
    path('editprofile/', views.edituserProfile, name='user_edit_profile'),
    path('profile-list/', views.userProfile, name='profile_list'),
    path('profile/make/default/<int:profile_id>', views.defaultAddress, name='defaultaddress'),
]