# Generated by Django 4.1 on 2023-11-21 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('haileapp', '0002_remove_extendedanswerquestion_question_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='haileuser',
            name='final_score',
            field=models.IntegerField(default=0),
        ),
    ]
