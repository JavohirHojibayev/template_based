from django.db import migrations


def seed_category(apps, schema_editor):
    Category = apps.get_model("blog", "Category")
    if not Category.objects.filter(slug="umumiy").exists():
        Category.objects.create(name="Umumiy", slug="umumiy")


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_category, migrations.RunPython.noop),
    ]
