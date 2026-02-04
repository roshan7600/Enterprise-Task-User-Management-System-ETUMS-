from rest_framework import serializers
from .models import Task


# ----------------------------------
# SINGLE TASK SERIALIZER
# ----------------------------------
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("created_by", "created_at", "updated_at")

    def validate(self, attrs):
        request = self.context["request"]

        # Employees cannot create or assign tasks
        if request.user.role == "EMPLOYEE":
            raise serializers.ValidationError(
                "Employees cannot create or assign tasks."
            )

        return attrs


# ----------------------------------
# BULK TASK CREATE SERIALIZER
# ----------------------------------
class BulkTaskSerializer(serializers.Serializer):
    tasks = TaskSerializer(many=True)

    def validate(self, attrs):
        request = self.context["request"]

        # Employees cannot bulk create tasks
        if request.user.role == "EMPLOYEE":
            raise serializers.ValidationError(
                "Employees cannot create or assign tasks."
            )

        return attrs

    def create(self, validated_data):
        tasks_data = validated_data["tasks"]
        user = self.context["request"].user

        task_objects = [
            Task(
                title=task["title"],
                description=task.get("description", ""),
                assigned_to=task["assigned_to"],
                created_by=user
            )
            for task in tasks_data
        ]

        return Task.objects.bulk_create(task_objects)


# ----------------------------------
# CSV FILE UPLOAD VALIDATION SERIALIZER
# ----------------------------------
class TaskCSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, file):
        if not file.name.lower().endswith(".csv"):
            raise serializers.ValidationError("Only CSV files are allowed.")
        return file
