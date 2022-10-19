from django.urls import path
from . import views


urlpatterns = [
    path('', views.landingpage, name="landingpage"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path('verify', views.verify, name="verify")
]
