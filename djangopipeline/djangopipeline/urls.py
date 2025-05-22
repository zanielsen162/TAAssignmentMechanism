"""
URL configuration for djangopipeline project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path
from . import views

urlpatterns = [
    path("application/", include("application.urls")),
    path("admin/", admin.site.urls),
    path('professors/', views.professor_list, name='professor_list'),
    path('professors/<int:pk>/', views.professor_detail, name='professor_detail'),
    path('professors/add/', views.professor_add, name='professor_add'),
    path('professors/<int:pk>/edit/', views.professor_edit, name='professor_edit'),
    path("", views.login, name="login"),
]
