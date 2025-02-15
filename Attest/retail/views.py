from rest_framework import generics
from .models import NetworkNode
from .serializers import NetworkNodeSerializer

class NetworkNodeListCreate(generics.ListCreateAPIView):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer

class NetworkNodeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
