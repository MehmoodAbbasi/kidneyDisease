from django.urls import path
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),


]