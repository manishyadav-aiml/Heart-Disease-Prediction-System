from io import BytesIO
from reportlab.pdfgen import canvas
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from . import ml
from .forms import PredictionForm, RegisterForm, describe
from .models import PredictionRecord

ADVICE = {
    "LOW": "The model estimates a low probability. Keep up healthy habits and have regular check-ups.",
    "MODERATE": "The model estimates a moderate probability. Consider a medical check-up and review lifestyle factors such as diet, exercise and smoking.",
    "HIGH": "The model estimates a high probability. Please consult a qualified doctor for proper tests and advice.",
}


def home(request):
    recent = []
    if request.user.is_authenticated:
        recent = request.user.predictions.all()[:5]
    return render(request, "prediction/home.html", {"recent": recent})


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Welcome, {user.username}! Your account has been created.")
        return redirect("predict")
    return render(request, "prediction/register.html", {"form": form})


@login_required
def predict(request):
    form = PredictionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        try:
            probability = ml.predict_probability(data)
        except ml.ModelNotAvailable as exc:
            messages.error(request, str(exc))
            return render(request, "prediction/prediction.html", {"form": form})

        record = PredictionRecord.objects.create(
            user=request.user,
            probability=round(probability * 100, 1),
            risk_level=ml.risk_level(probability),
            **data,
        )
        return redirect("result", pk=record.pk)
    return render(request, "prediction/prediction.html", {"form": form})


@login_required
def result(request, pk):
    record = get_object_or_404(PredictionRecord, pk=pk, user=request.user)
    context = {
        "record": record,
        "rows": describe(record),
        "advice": ADVICE[record.risk_level],
        "level_class": record.risk_level.lower(),
    }
    return render(request, "prediction/result.html", context)
@login_required
def download_pdf(request, pk):
    record = get_object_or_404(PredictionRecord, pk=pk, user=request.user)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.setTitle("Heart Disease Risk Prediction")

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, 800, "Heart Disease Risk Prediction")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 770, f"Risk Level: {record.risk_level}")
    pdf.drawString(50, 750, f"Probability: {record.probability}%")

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, 710, "Patient Information")

    y = 685
    pdf.setFont("Helvetica", 10)

    for label, value in describe(record):
        pdf.drawString(60, y, f"{label}: {value}")
        y -= 20

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y - 10, "Advice")

    pdf.setFont("Helvetica", 10)
    y -= 30

    for line in ADVICE[record.risk_level].split(". "):
        pdf.drawString(60, y, line)
        y -= 15

    pdf.setFont("Helvetica-Oblique", 9)
    pdf.drawString(
        50,
        80,
        "This report is a screening aid only and is not a medical diagnosis."
    )

    pdf.save()

    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="heart_disease_report_{record.pk}.pdf"'
    )

    return response

