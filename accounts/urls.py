from django.urls import path
from accounts import views

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/edit/", views.ProfileEditView.as_view(), name="profile_edit"),
    path("login/", views.LoginView.as_view(), name="account_login"),
    path("logout/", views.LogoutView.as_view(), name="account_logout"),
    path("signup/", views.SignupView.as_view(), name="account_signup"),
]
