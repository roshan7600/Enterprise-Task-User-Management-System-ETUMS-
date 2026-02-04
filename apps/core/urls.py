from django.urls import path, include
from .views import ProtectedView

urlpatterns = [
    # Core / common APIs
    path('protected/', ProtectedView.as_view()),

    # Feature apps
    path('', include('apps.tasks.urls')),
]
