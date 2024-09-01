"""
URL configuration for django_permission project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from base import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cu/',views.UserCreateUpdateView.as_view(), name='create_user'),
    path('assign-permission/', views.AssignPermissionView.as_view(), name='assign-permission'),
    path('create-transactions/', views.CreateTransactionView.as_view(), name='create-transactions'),
    path('create-transactions/<int:pk>/', views.CreateTransactionView.as_view(), name='create-transactions'),
    path('f1',views.Get_particular_user_permission),
    path('all-permission',views.AllModelPermissionsView.as_view()),
    path('api-auth/', include('rest_framework.urls'))
]
