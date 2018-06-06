# Generated by Django 2.0.5 on 2018-06-05 21:42

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20180601_2147'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('product_name', models.CharField(max_length=50)),
                ('file', models.FileField(null=True, upload_to='')),
                ('img', models.ImageField(blank=True, null=True, upload_to=accounts.models.product_img_uh)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
    ]
