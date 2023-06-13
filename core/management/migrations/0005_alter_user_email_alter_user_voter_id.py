# Generated by Django 4.2.1 on 2023-06-13 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0004_alter_user_email_alter_user_voter_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                default="7682064@gmail.com", max_length=255, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="voter_id",
            field=models.CharField(
                blank=True, default="7682064", max_length=10, unique=True
            ),
        ),
    ]
