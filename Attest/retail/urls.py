from django.urls import path
from . import views

urlpatterns = [
    path('nodes/', views.NetworkNodeListCreate.as_view(), name='node-list'),
    path('nodes/<int:pk>/', views.NetworkNodeRetrieveUpdateDestroy.as_view(), name='node-detail'),
]