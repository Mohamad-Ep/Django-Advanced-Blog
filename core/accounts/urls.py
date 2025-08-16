from django.urls import path, include
from . import views

# __________________________________________________________

app_name = "accounts"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("index/", views.IndexView.as_view(), name="accounts-index"),
    path("send-email/", views.send_Email, name="send-email"),
    path("mock-server/", views.test_mock, name="mock-server"),
    path("api/v1/", include("accounts.api.v1.urls", namespace="api-v1"), name="api-v1"),
    path("api/v2/", include("djoser.urls")),  # add api/v2 by djoser
    path("api/v2/", include("djoser.urls.jwt")),  # add api/v2 by djoser
]

# __________________________________________________________
