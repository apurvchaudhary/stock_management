from django.core.management.base import BaseCommand

from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "get or create default superuser"

    def handle(self, *args, **kwargs):
        user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@mail.com",
                "password": "admin1234",
                "first_name": "Admin",
                "last_name": "admin",
            },
        )
        if created:
            user.set_password("admin1234")
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"super user created successfully"))
