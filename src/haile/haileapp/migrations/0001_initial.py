# Generated by Django 4.1 on 2023-10-24 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HaileUser",
            fields=[
                ("user_id", models.AutoField(primary_key=True, serialize=False)),
                ("firstname", models.CharField(max_length=100)),
                ("surname", models.CharField(max_length=100)),
                ("email", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=100)),
                ("final_score", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                ("question_id", models.AutoField(primary_key=True, serialize=False)),
                ("question_type", models.CharField(max_length=50)),
                ("question_text", models.TextField()),
                ("correct_answer", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Quiz",
            fields=[
                ("quiz_id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Response",
            fields=[
                ("response_id", models.AutoField(primary_key=True, serialize=False)),
                ("text", models.TextField()),
                ("is_correct", models.BooleanField()),
                (
                    "question_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="haileapp.question",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="haileapp.haileuser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ChatPrompt",
            fields=[
                ("prompt_id", models.AutoField(primary_key=True, serialize=False)),
                ("prompt_text", models.TextField()),
                ("section_from", models.CharField(max_length=100)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="haileapp.haileuser",
                    ),
                ),
            ],
        ),
    ]
