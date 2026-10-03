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
    "LOW": (
        "The model estimates a low probability. "
        "Keep up healthy habits and have regular check-ups."
    ),
    "MODERATE": (
        "The model estimates a moderate probability. "
        "Consider a medical check-up and review lifestyle factors "
        "such as diet, exercise and smoking."
    ),
    "HIGH": (
        "The model estimates a high probability. "
        "Please consult a qualified doctor for proper tests and advice."
    ),
}


def home(request):
    recent = []

    if request.user.is_authenticated:
        recent = request.user.predictions.all()[:5]

    return render(
        request,
        "prediction/home.html",
        {"recent": recent}
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()

        login(request, user)

        messages.success(
            request,
            f"Welcome, {user.username}! Your account has been created."
        )

        return redirect("predict")

    return render(
        request,
        "prediction/register.html",
        {"form": form}
    )


@login_required
def predict(request):
    form = PredictionForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        try:
            probability = ml.predict_probability(data)

        except ml.ModelNotAvailable as exc:
            messages.error(request, str(exc))

            return render(
                request,
                "prediction/prediction.html",
                {"form": form}
            )

        record = PredictionRecord.objects.create(
            user=request.user,
            probability=round(probability * 100, 1),
            risk_level=ml.risk_level(probability),
            **data,
        )

        return redirect("result", pk=record.pk)

    return render(
        request,
        "prediction/prediction.html",
        {"form": form}
    )


@login_required
def result(request, pk):
    record = get_object_or_404(
        PredictionRecord,
        pk=pk,
        user=request.user
    )

    context = {
        "record": record,
        "rows": describe(record),
        "advice": ADVICE[record.risk_level],
        "level_class": record.risk_level.lower(),
    }

    return render(
        request,
        "prediction/result.html",
        context
    )


@login_required
def download_pdf(request, pk):
    record = get_object_or_404(
        PredictionRecord,
        pk=pk,
        user=request.user
    )

    buffer = BytesIO()

    # A4 page size
    page_width = 595
    page_height = 842

    pdf = canvas.Canvas(
        buffer,
        pagesize=(page_width, page_height)
    )

    pdf.setTitle(
        "Heart Disease Risk Assessment Report"
    )

    pdf.setAuthor(
        "Heart Disease Prediction System"
    )

    # =========================================================
    # HEADER
    # =========================================================

    pdf.setFillColorRGB(
        0.08,
        0.25,
        0.45
    )

    pdf.rect(
        0,
        760,
        page_width,
        82,
        fill=1,
        stroke=0
    )

    pdf.setFillColorRGB(
        1,
        1,
        1
    )

    pdf.setFont(
        "Helvetica-Bold",
        21
    )

    pdf.drawString(
        40,
        810,
        "HEARTCARE"
    )

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        40,
        792,
        "Heart Disease Risk Assessment"
    )

    pdf.setFont(
        "Helvetica",
        9
    )

    pdf.drawRightString(
        page_width - 40,
        810,
        f"Report ID: HD-{record.pk:05d}"
    )

    pdf.drawRightString(
        page_width - 40,
        792,
        "Assessment Type: Machine Learning Screening"
    )

    # =========================================================
    # PATIENT NAME
    # =========================================================

    pdf.setFont(
        "Helvetica-Bold",
        9
    )

    pdf.drawRightString(
        page_width - 40,
        775,
        f"Patient Name: {record.user.username}"
    )

    # =========================================================
    # ASSESSMENT RESULT
    # =========================================================

    y = 730

    pdf.setFillColorRGB(
        0.15,
        0.15,
        0.15
    )

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawString(
        40,
        y,
        "ASSESSMENT RESULT"
    )

    y -= 25

    # Result card
    pdf.setFillColorRGB(
        0.95,
        0.97,
        0.99
    )

    pdf.roundRect(
        40,
        y - 100,
        page_width - 80,
        95,
        10,
        fill=1,
        stroke=0
    )

    # Risk level
    pdf.setFillColorRGB(
        0.08,
        0.25,
        0.45
    )

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        60,
        y - 30,
        "RISK LEVEL"
    )

    pdf.setFont(
        "Helvetica-Bold",
        27
    )

    pdf.drawString(
        60,
        y - 67,
        str(record.risk_level)
    )

    # Probability
    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        300,
        y - 30,
        "ESTIMATED PROBABILITY"
    )

    pdf.setFont(
        "Helvetica-Bold",
        27
    )

    pdf.drawString(
        300,
        y - 67,
        f"{record.probability}%"
    )

    pdf.setFont(
        "Helvetica",
        8
    )

    pdf.setFillColorRGB(
        0.35,
        0.35,
        0.35
    )

    pdf.drawString(
        60,
        y - 88,
        "Result generated using the trained machine learning model."
    )

    # =========================================================
    # PATIENT INFORMATION
    # =========================================================

    y -= 135

    pdf.setFillColorRGB(
        0.15,
        0.15,
        0.15
    )

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        40,
        y,
        "PATIENT INFORMATION"
    )

    y -= 20

    # Patient name as the first patient-information row
    rows = [
        ("Patient Name", record.user.username),
        *describe(record),
    ]

    table_x = 40
    table_width = page_width - 80
    row_height = 22
    label_width = 220

    for index, (label, value) in enumerate(rows):

        # Alternate row background
        if index % 2 == 0:

            pdf.setFillColorRGB(
                0.96,
                0.97,
                0.98
            )

            pdf.rect(
                table_x,
                y - row_height + 4,
                table_width,
                row_height,
                fill=1,
                stroke=0
            )

        pdf.setFillColorRGB(
            0.12,
            0.12,
            0.12
        )

        pdf.setFont(
            "Helvetica-Bold",
            9
        )

        pdf.drawString(
            table_x + 10,
            y - 10,
            str(label)
        )

        pdf.setFont(
            "Helvetica",
            9
        )

        pdf.drawString(
            table_x + label_width,
            y - 10,
            str(value)
        )

        # Bottom border
        pdf.setStrokeColorRGB(
            0.85,
            0.85,
            0.85
        )

        pdf.line(
            table_x,
            y - row_height + 3,
            table_x + table_width,
            y - row_height + 3
        )

        y -= row_height

    # =========================================================
    # MODEL INTERPRETATION
    # =========================================================

    y -= 20

    pdf.setFillColorRGB(
        0.15,
        0.15,
        0.15
    )

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        40,
        y,
        "MODEL INTERPRETATION"
    )

    y -= 22

    pdf.setFillColorRGB(
        0.98,
        0.98,
        0.98
    )

    pdf.roundRect(
        40,
        y - 62,
        page_width - 80,
        58,
        7,
        fill=1,
        stroke=1
    )

    pdf.setFillColorRGB(
        0.2,
        0.2,
        0.2
    )

    pdf.setFont(
        "Helvetica",
        9
    )

    advice = ADVICE[record.risk_level]

    # Wrap advice text
    words = advice.split()

    line = ""
    lines = []

    for word in words:

        test_line = f"{line} {word}".strip()

        if pdf.stringWidth(
            test_line,
            "Helvetica",
            9
        ) < 490:

            line = test_line

        else:

            lines.append(line)
            line = word

    if line:
        lines.append(line)

    advice_y = y - 22

    for line in lines:

        pdf.drawString(
            55,
            advice_y,
            line
        )

        advice_y -= 14

    # =========================================================
    # MODEL DETAILS
    # =========================================================

    y -= 90

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.setFillColorRGB(
        0.15,
        0.15,
        0.15
    )

    pdf.drawString(
        40,
        y,
        "MODEL DETAILS"
    )

    y -= 22

    model_details = [
        (
            "Algorithm",
            "Random Forest Classifier"
        ),
        (
            "Input Features",
            "13"
        ),
        (
            "Validation",
            "5-Fold Stratified Cross-Validation"
        ),
        (
            "Application",
            "Django Web Application"
        ),
    ]

    for label, value in model_details:

        pdf.setFont(
            "Helvetica-Bold",
            9
        )

        pdf.drawString(
            50,
            y,
            f"{label}:"
        )

        pdf.setFont(
            "Helvetica",
            9
        )

        pdf.drawString(
            170,
            y,
            value
        )

        y -= 17

    # =========================================================
    # DISCLAIMER BOX
    # =========================================================

    y -= 12

    pdf.setFillColorRGB(
        1,
        0.97,
        0.88
    )

    pdf.roundRect(
        40,
        y - 75,
        page_width - 80,
        70,
        7,
        fill=1,
        stroke=0
    )

    pdf.setFillColorRGB(
        0.45,
        0.30,
        0.05
    )

    pdf.setFont(
        "Helvetica-Bold",
        9
    )

    pdf.drawString(
        52,
        y - 22,
        "IMPORTANT DISCLAIMER"
    )

    pdf.setFont(
        "Helvetica",
        8
    )

    disclaimer_lines = [
        "This report is generated by a machine learning system for educational",
        "and screening purposes only. It is not a medical diagnosis or a substitute",
        "for professional medical advice, examination, or treatment."
    ]

    disclaimer_y = y - 37

    for line in disclaimer_lines:

        pdf.drawString(
            52,
            disclaimer_y,
            line
        )

        disclaimer_y -= 12

    # =========================================================
    # FOOTER
    # =========================================================

    pdf.setStrokeColorRGB(
        0.82,
        0.82,
        0.82
    )

    pdf.line(
        40,
        48,
        page_width - 40,
        48
    )

    pdf.setFillColorRGB(
        0.4,
        0.4,
        0.4
    )

    pdf.setFont(
        "Helvetica-Bold",
        8
    )

    pdf.drawCentredString(
        page_width / 2,
        32,
        "Disclaimer: This report is not a medical diagnosis."
    )

    # =========================================================
    # FINISH PDF
    # =========================================================

    pdf.save()

    buffer.seek(0)

    response = HttpResponse(
        buffer,
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="heart_disease_report_{record.pk}.pdf"'
    )

    return response