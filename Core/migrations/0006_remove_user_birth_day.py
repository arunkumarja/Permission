# Generated by Django 4.2.11 on 2024-05-30 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0005_alter_user_birth_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='birth_day',
        ),
    ]