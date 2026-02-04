from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsAdmin


class ProtectedView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({
            "message": "Admin access granted",
            "user": request.user.email,
            "role": request.user.role
        })
