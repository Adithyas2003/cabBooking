# Generated by Django 5.1.6 on 2025-02-20 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_booking_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Full_name', models.CharField(max_length=255)),
                ('email_address', models.EmailField(max_length=255)),
                ('message', models.CharField(max_length=255)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
