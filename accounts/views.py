from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import login, logout
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['post'])
    def login(self, request):
        if request.user.is_authenticated:
            return Response({'detail': 'Already logged in'})
        user = User.objects.get(email=request.data['email'])
        if user.check_password(request.data['password']):
            login(request, user)
            return Response({'detail': 'Successfully logged in'})
        return Response({'detail': 'Invalid credentials'}, status=400)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({'detail': 'Successfully logged out'})
        return Response({'detail': 'Not logged in'}, status=400)
