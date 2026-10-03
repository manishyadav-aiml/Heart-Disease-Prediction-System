import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PredictionRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("age", models.PositiveSmallIntegerField()),
                ("sex", models.PositiveSmallIntegerField()),
                ("cp", models.PositiveSmallIntegerField()),
                ("trestbps", models.PositiveSmallIntegerField()),
                ("chol", models.PositiveSmallIntegerField()),
                ("fbs", models.PositiveSmallIntegerField()),
                ("restecg", models.PositiveSmallIntegerField()),
                ("thalach", models.PositiveSmallIntegerField()),
                ("exang", models.PositiveSmallIntegerField()),
                ("oldpeak", models.FloatField()),
                ("slope", models.PositiveSmallIntegerField()),
                ("ca", models.PositiveSmallIntegerField()),
                ("thal", models.PositiveSmallIntegerField()),
                ("probability", models.FloatField(help_text="Predicted probability of heart disease, in percent")),
                ("risk_level", models.CharField(max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="predictions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
