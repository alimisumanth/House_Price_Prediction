# Generated by Django 3.2.3 on 2021-06-05 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pr1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
