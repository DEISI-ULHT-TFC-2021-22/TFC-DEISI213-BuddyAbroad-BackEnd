# Generated by Django 4.0.1 on 2022-04-17 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buddyAbroadAPI', '0010_interests_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='guide',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
