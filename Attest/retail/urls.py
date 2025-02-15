from django.urls import path
from rest_framework.permissions import AllowAny

from . import views

urlpatterns = [
    path('nodes/', views.NetworkNodeListCreate.as_view(permission_classes=(AllowAny,)), name='node-list'),
    path('nodes/<int:pk>/', views.NetworkNodeRetrieveUpdateDestroy.as_view(permission_classes=(AllowAny,)), name='node-detail'),
]