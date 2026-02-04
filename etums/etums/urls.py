from django.contrib import admin
from django.urls import path, include
from apps.accounts.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)



urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Auth (ONLY ONCE)
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Core APIs
    path('api/', include('apps.core.urls')),


# GET /api/users/
#  GET /api/users/?role=EMPLOYEE

    path("api/", include("apps.accounts.urls")),


    # 🔹 OpenAPI schema (raw JSON)
    # Used internally by Swagger / Redoc

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),


    # 🔹 Swagger UI (interactive API documentation)
    # Visit: http://127.0.0.1:8000/api/docs/
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
