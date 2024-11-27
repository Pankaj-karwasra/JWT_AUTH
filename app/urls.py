from django.urls import path
from app import views
from app.views import UserRegistration,UserLoginView,UserProfileView,UserChangePassword,SendPasswordEmailView,UserPasswordResetView


urlpatterns = [
   
    path("register/",UserRegistration.as_view(),name='register'),
    path("login/",UserLoginView.as_view(),name='login'),
    path("profile/",UserProfileView.as_view(),name='profile'),
    path("changepassword/",UserChangePassword.as_view(),name='changepassword'),
    path('send-reset-password-email/',SendPasswordEmailView.as_view(),name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name='reset-password')

]