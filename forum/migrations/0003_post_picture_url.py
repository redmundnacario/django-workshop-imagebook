# Generated by Django 3.2.4 on 2021-06-24 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20210624_0424'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='picture_url',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
