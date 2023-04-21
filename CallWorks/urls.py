"""CallWorks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from webapp.sample_views import SampleView
from webapp.views import CallWorksLoginView, UserProfileView, CustomizedAdminLoginView, logout, DashboardView

urlpatterns = [
    # path('login/', RedirectView.as_view(pattern_name='accounts-login')),
    # path('accounts/login/', CallWorksLoginView.as_view(), name="accounts-login"), # TODO email/pass login not working

    path('accounts/login/', RedirectView.as_view(pattern_name='login')),
    path('accounts/profile/', UserProfileView.as_view(), name="profile"),

    path('login/', CustomizedAdminLoginView.as_view(), name='login'),
    path('logout', logout, name='logout'),

    path('admin/', admin.site.urls),

    path('', RedirectView.as_view(pattern_name='dashboard'), name="index"),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('sample/', SampleView.as_view())
]
