# Generated by Django 4.2.11 on 2024-05-30 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0004_user_birth_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_day',
            field=models.DateField(null=True),
        ),
    ]