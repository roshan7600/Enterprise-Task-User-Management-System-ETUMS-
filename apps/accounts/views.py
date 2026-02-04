import logging

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    CustomTokenObtainPairSerializer,
    UserCreateSerializer,
)
from .throttles import LoginRateThrottle
from .models import User

from rest_framework.permissions import IsAdminUser



logger = logging.getLogger("apps")


# 🔐 Login API (JWT + Throttling + Logging)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [LoginRateThrottle]

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            logger.warning(
                f"Login failed | email={request.data.get('email')} | error={str(e)}"
            )
            raise


# 👤 Users API (Admin-only CRUD)
class UserViewSet(ModelViewSet):
    """
    Admin-only User Management API
    - List users
    - Create users
    - Update users
    - Delete users
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
