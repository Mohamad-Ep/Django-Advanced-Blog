from django.urls import path, include
from .. import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# __________________________________________________________

urlpatterns = [
    # login token
    path("registeration/", views.RegisterationApiView.as_view(), name="registeration"),
    # path('token/login/', ObtainAuthToken.as_view(), name='token-login'),
    path("token/login/", views.CustomAuthToken.as_view(), name="token-login"),
    path("token/logout/", views.CustomDicardAthToken.as_view(), name="token-logout"),
    # activation
    path(
        "activation/confirm/<str:token>/",
        views.ActivationApiView.as_view(),
        name="activation",
    ),
    # activation resend
    path(
        "activation/resend/",
        views.ResendActivationApiView.as_view(),
        name="activation-resend",
    ),
    # reset password
    # login jwt
    # path('jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    # change-password
    path(
        "change-password/",
        views.ChangePasswordApiView.as_view(),
        name="change-password",
    ),
    # test email send
    path("test-email/", views.TestEmailSend.as_view(), name="test-email"),
]

# __________________________________________________________
