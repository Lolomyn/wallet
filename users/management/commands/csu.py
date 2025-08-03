from django.core.management import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        username = "admin"

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create(username=username)
            user.set_password("admin")
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
