# Generated by Django 3.2 on 2021-05-17 21:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0008_client_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='due_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default_profile.jpg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='client',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
