# Generated by Django 3.2 on 2021-05-04 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_movie_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
