from django.conf import settings
from django.db import models


class PredictionRecord(models.Model):
    """One heart disease risk prediction made by a registered user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="predictions",
    )

    # The 13 input attributes (same names as the columns of heart.csv)
    age = models.PositiveSmallIntegerField()
    sex = models.PositiveSmallIntegerField()
    cp = models.PositiveSmallIntegerField()
    trestbps = models.PositiveSmallIntegerField()
    chol = models.PositiveSmallIntegerField()
    fbs = models.PositiveSmallIntegerField()
    restecg = models.PositiveSmallIntegerField()
    thalach = models.PositiveSmallIntegerField()
    exang = models.PositiveSmallIntegerField()
    oldpeak = models.FloatField()
    slope = models.PositiveSmallIntegerField()
    ca = models.PositiveSmallIntegerField()
    thal = models.PositiveSmallIntegerField()

    # Result
    probability = models.FloatField(help_text="Predicted probability of heart disease, in percent")
    risk_level = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.risk_level} ({self.probability:.1f}%)"
