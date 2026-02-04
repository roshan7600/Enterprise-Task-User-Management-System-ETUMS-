from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Task(models.Model):

    class Status(models.TextChoices):
        TODO = "TODO", "To Do"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        DONE = "DONE", "Done"
        OVERDUE = "OVERDUE", "Overdue"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_tasks"
    )

    # NEW FIELDS
    due_date = models.DateField(null=True, blank=True)
    is_overdue = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["assigned_to"]),
            models.Index(fields=["created_by"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["is_overdue"]),
            models.Index(fields=["due_date"]),
        ]

    def check_overdue(self):
        """
        Check and mark task as overdue if due_date has passed
        """
        if self.due_date and self.due_date < timezone.now().date():
            if not self.is_overdue:
                self.is_overdue = True
                self.status = self.Status.OVERDUE
                self.save(update_fields=["is_overdue", "status"])
            return True
        return False

    def save(self, *args, **kwargs):
        """
        Automatically update overdue status on save
        """
        if self.due_date and self.due_date < timezone.now().date():
            self.is_overdue = True
            self.status = self.Status.OVERDUE
        else:
            self.is_overdue = False

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
