from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

from django.contrib import admin
from django.urls import path, include
from core import views as core_views

from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/login/",  LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("accounts/logout/", LogoutView.as_view(next_page="home"), name="logout"),  # 👈 force redirect
    path("accounts/signup/", core_views.signup, name="signup"),
]
