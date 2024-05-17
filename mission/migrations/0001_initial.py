# Generated by Django 5.0.6 on 2024-05-15 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('date', models.DateField()),
                ('is_successful', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, upload_to='mission_images/')),
                ('category', models.CharField(max_length=100)),
            ],
        ),
    ]