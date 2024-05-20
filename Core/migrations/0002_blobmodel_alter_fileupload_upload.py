# Generated by Django 4.2.11 on 2024-05-20 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlobModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blob', models.BinaryField()),
                ('name', models.CharField(max_length=200)),
                ('upload_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='upload',
            field=models.FileField(upload_to=''),
        ),
    ]