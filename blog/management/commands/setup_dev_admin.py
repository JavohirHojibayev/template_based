from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Yaratadi yoki yangilaydi: username=admin, parol=admin, staff va superuser. "
        "Faqat mahalliy rivojlantirish uchun."
    )

    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        user.is_staff = True
        user.is_superuser = True
        user.email = user.email or "admin@example.com"
        user.set_password("admin")
        user.save()
        if created:
            self.stdout.write(self.style.SUCCESS('Foydalanuvchi "admin" yaratildi (parol: admin).'))
        else:
            self.stdout.write(self.style.SUCCESS('Foydalanuvchi "admin" yangilandi (parol: admin, staff/superuser).'))
