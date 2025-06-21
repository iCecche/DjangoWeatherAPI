from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from .serializer import UserRegisterSerializer

class UserViewSet(ViewSet):
    permission_classes = []
    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        POST /api/users/register/
        Registra un nuovo utente
        """
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Registrazione completata."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)