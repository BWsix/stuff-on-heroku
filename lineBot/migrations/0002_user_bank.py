# Generated by Django 3.1.7 on 2021-03-15 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lineBot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bank',
            field=models.IntegerField(default=0),
        ),
    ]
