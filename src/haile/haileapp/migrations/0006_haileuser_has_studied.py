# Generated by Django 4.1 on 2024-01-05 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('haileapp', '0005_extendedanswerresponse_user_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='haileuser',
            name='has_studied',
            field=models.BooleanField(default=False),
        ),
    ]
