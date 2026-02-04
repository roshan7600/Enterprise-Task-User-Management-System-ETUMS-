from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.tasks.models import Task

class Command(BaseCommand):
    help = "Mark overdue tasks and send reminders"

    def handle(self, *args, **options):
        today = timezone.now().date()

        overdue_tasks = Task.objects.filter(
            due_date__lt=today,
            is_overdue=False,
            status__in=["TODO", "IN_PROGRESS"],
        )

        count = overdue_tasks.count()

        overdue_tasks.update(is_overdue=True)

        self.stdout.write(
            self.style.SUCCESS(f"{count} tasks marked as overdue")
        )
