# Generated by Django 3.1 on 2021-05-25 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210525_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='https://www.w3schools.com/howto/img_avatar.png', null=True, upload_to='userproflie'),
        ),
    ]
