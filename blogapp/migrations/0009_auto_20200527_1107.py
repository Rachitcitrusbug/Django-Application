# Generated by Django 3.0.6 on 2020-05-27 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0008_auto_20200527_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='sample.jpg', upload_to=''),
        ),
    ]
