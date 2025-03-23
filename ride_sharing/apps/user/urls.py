from apps.user.api.views import LoginAPIView, LogoutAPIView, RegistrationAPIView
from django.urls import path

urlpatterns = [
    path("onboard/", RegistrationAPIView.as_view(), name="authentication.rest_login"),
    path("login/", LoginAPIView.as_view(), name="authentication.rest_login"),
    path("logout/", LogoutAPIView.as_view(), name="authentication.logout"),
]
