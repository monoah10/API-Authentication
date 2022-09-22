from django.urls import path
from account.views import UserChangePasswordView, UserProfileView, UserRegistrationView,UserLoginView,SendPasswordRestEmailView, UserRestPasswordView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('profile/', UserProfileView.as_view(),name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(),name='changepassword'),
    path('link-email/', SendPasswordRestEmailView.as_view(),name='link-email'),
    path('rest-password/<uid>/<token>/', UserRestPasswordView.as_view(),name='rest-password'),
]