# Generated by Django 4.0.1 on 2022-01-21 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0003_rename_image_info_imag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='imag',
            field=models.ImageField(default='default.png', upload_to='static/profile_image'),
        ),
    ]
