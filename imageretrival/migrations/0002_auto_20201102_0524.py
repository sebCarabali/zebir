# Generated by Django 3.0.5 on 2020-11-02 05:24

from django.db import migrations, models
import imageretrival.models


class Migration(migrations.Migration):

    dependencies = [
        ('imageretrival', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(upload_to=imageretrival.models.user_upload_dir),
        ),
    ]
