from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    path("", views.home, name="home"),

    path("register/", views.register, name="register"),

    # Login
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="prediction/login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),

    # Logout
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    # Forgot Password
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="prediction/password_reset.html"
        ),
        name="password_reset",
    ),

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="prediction/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="prediction/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),

    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="prediction/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),

    # Prediction
    path("predict/", views.predict, name="predict"),

    # Result
    path("result/<int:pk>/", views.result, name="result"),

    # PDF Report
    path(
        "result/<int:pk>/pdf/",
        views.download_pdf,
        name="download_pdf",
    ),
]