# Generated by Django 4.2.7 on 2024-08-21 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_user_followers_user_following_post_like_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='following',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
