import logging
logger=logging.getLogger("apps")


import csv
from io import TextIOWrapper

from django.db import transaction
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from apps.accounts.models import User
from .models import Task
from .serializers import (
    TaskSerializer,
    BulkTaskSerializer,
    TaskCSVUploadSerializer,
)
from .permissions import IsAdminOrManager


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    # -----------------------------
    # FILTERING & ORDERING
    # -----------------------------
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status", "assigned_to"]
    ordering_fields = ["created_at", "status"]
    ordering = ["-created_at"]

    # -----------------------------
    # OPTIMIZED ROLE-BASED QUERYSET
    # -----------------------------
    def get_queryset(self):
        user = self.request.user

        qs = Task.objects.select_related(
            "assigned_to",
            "created_by",
        )

        if user.role == "ADMIN":
            return qs

        if user.role == "MANAGER":
            return qs.filter(created_by=user)

        return qs.filter(assigned_to=user)

    # -----------------------------
    # CACHED TASK LIST
    # -----------------------------
    def list(self, request, *args, **kwargs):
        cache_key = f"tasks_list_user_{request.user.id}"
        cached = cache.get(cache_key)

        if cached:
            return Response(cached)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60)
        return response

    # -----------------------------
    # CREATE TASK
    # -----------------------------
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        cache.delete(f"tasks_list_user_{self.request.user.id}")

    # -----------------------------
    # UPDATE TASK
    # EMPLOYEE → STATUS ONLY
    # -----------------------------
    # def update(self, request, *args, **kwargs):
    #     task = self.get_object()
    #     user = request.user

    #     if user.role == "EMPLOYEE":
    #         if task.assigned_to != user or list(request.data.keys()) != ["status"]:
    #             return Response(
    #                 {"detail": "You can only update task status."},
    #                 status=status.HTTP_403_FORBIDDEN,
    #             )

    #     response = super().update(request, *args, **kwargs)
    #     cache.delete(f"tasks_list_user_{request.user.id}")
    #     return response

    def update(self, request, *args, **kwargs):
         
     try:
        user = request.user
        task = self.get_object()

        # EMPLOYEE can update ONLY status
        if user.role == "EMPLOYEE":
            if task.assigned_to != user or list(request.data.keys()) != ["status"]:
                return Response(
                    {"detail": "You can only update task status."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        response = super().update(request, *args, **kwargs)
        return response

     except Exception as e:
        logger.error(
            f"Task update failed | user={request.user.id} | error={str(e)}"
        )
        raise


    # -----------------------------
    # DELETE TASK
    # -----------------------------
    def perform_destroy(self, instance):
        instance.delete()
        cache.delete(f"tasks_list_user_{self.request.user.id}")

    # -----------------------------
    # PERMISSIONS BY ACTION
    # -----------------------------
    def get_permissions(self):
        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
            "bulk_create",
            "bulk_upload",
        ]:
            return [IsAuthenticated(), IsAdminOrManager()]
        return super().get_permissions()

    # -----------------------------
    # BULK CREATE (JSON)
    # -----------------------------
    @action(detail=False, methods=["post"], url_path="bulk-create")
    def bulk_create(self, request):
        serializer = BulkTaskSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        cache.delete(f"tasks_list_user_{request.user.id}")

        return Response(
            {"message": "Tasks created successfully"},
            status=status.HTTP_201_CREATED,
        )

    # -----------------------------
    # BULK UPLOAD (CSV) 
    # -----------------------------
    # @action(detail=False, methods=["post"], url_path="bulk-upload")
    # def bulk_upload(self, request):
    #     serializer = TaskCSVUploadSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     file = serializer.validated_data["file"]
    #     user = request.user

    #     reader = csv.DictReader(TextIOWrapper(file, encoding="utf-8"))
    #     tasks_buffer = []
    #     created_count = 0
    #     BATCH_SIZE = 1000

    #     valid_user_ids = set(
    #         User.objects.values_list("id", flat=True)
    #     )

    #     with transaction.atomic():
    #         for line_no, row in enumerate(reader, start=2):
    #             if not row.get("title") or not row.get("assigned_to"):
    #                 continue

    #             assigned_to_id = int(row["assigned_to"])

    #             if assigned_to_id not in valid_user_ids:
    #                 raise ValidationError(
    #                     f"Invalid assigned_to ID {assigned_to_id} at line {line_no}"
    #                 )

    #             tasks_buffer.append(
    #                 Task(
    #                     title=row["title"],
    #                     description=row.get("description", ""),
    #                     status=row.get("status", Task.Status.TODO),
    #                     assigned_to_id=assigned_to_id,
    #                     created_by=user,
    #                 )
    #             )

    #             if len(tasks_buffer) >= BATCH_SIZE:
    #                 Task.objects.bulk_create(tasks_buffer)
    #                 created_count += len(tasks_buffer)
    #                 tasks_buffer.clear()

    #         if tasks_buffer:
    #             Task.objects.bulk_create(tasks_buffer)
    #             created_count += len(tasks_buffer)

    #     cache.delete(f"tasks_list_user_{request.user.id}")

    #     return Response(
    #         {"message": f"{created_count} tasks uploaded successfully"},
    #         status=status.HTTP_201_CREATED,
    #     )





    @action(detail=False, methods=["post"], url_path="bulk-upload")
    def bulk_upload(self, request):
        serializer = TaskCSVUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data["file"]
        user = request.user

        reader = csv.DictReader(TextIOWrapper(file, encoding="utf-8"))
        tasks_buffer = []
        created_count = 0
        BATCH_SIZE = 1000

        valid_user_ids = set(
            User.objects.values_list("id", flat=True)
        )

        try:
            with transaction.atomic():
                for line_no, row in enumerate(reader, start=2):
                    if not row.get("title") or not row.get("assigned_to"):
                        continue

                    try:
                        assigned_to_id = int(row["assigned_to"])
                    except ValueError:
                        raise ValidationError(
                            f"Invalid assigned_to value at line {line_no}"
                        )

                    if assigned_to_id not in valid_user_ids:
                        raise ValidationError(
                            f"Invalid assigned_to ID {assigned_to_id} at line {line_no}"
                        )

                    tasks_buffer.append(
                        Task(
                            title=row["title"],
                            description=row.get("description", ""),
                            status=row.get("status", Task.Status.TODO),
                            assigned_to_id=assigned_to_id,
                            created_by=user,
                        )
                    )

                    if len(tasks_buffer) >= BATCH_SIZE:
                        Task.objects.bulk_create(tasks_buffer)
                        created_count += len(tasks_buffer)
                        tasks_buffer.clear()

                if tasks_buffer:
                    Task.objects.bulk_create(tasks_buffer)
                    created_count += len(tasks_buffer)

        except ValidationError as e:
            logger.error(
                f"Bulk upload failed | user={request.user.id} | error={str(e)}"
            )
            raise

        cache.delete(f"tasks_list_user_{request.user.id}")

        return Response(
            {"message": f"{created_count} tasks uploaded successfully"},
            status=status.HTTP_201_CREATED,
        )