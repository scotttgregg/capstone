# Generated by Django 2.0.5 on 2018-05-30 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_blog_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='file',
            new_name='image',
        ),
    ]
