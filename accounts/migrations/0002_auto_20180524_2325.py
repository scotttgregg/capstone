# Generated by Django 2.0.5 on 2018-05-24 23:25

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_img',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.profile_img_uh),
        ),
    ]