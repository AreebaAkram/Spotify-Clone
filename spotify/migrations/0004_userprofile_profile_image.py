# Generated by Django 5.1.1 on 2024-12-22 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0003_remove_userprofile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(default='', upload_to='media/image'),
        ),
    ]
