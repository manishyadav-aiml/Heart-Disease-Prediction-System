from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .ml import FEATURES


class StyledFormMixin:
    """Adds the CSS class used by the site to every form widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css + " form-control").strip()


class RegisterForm(StyledFormMixin, UserCreationForm):
    email = forms.EmailField(required=True, help_text="Used only for your account.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )
        return email


class LoginForm(StyledFormMixin, AuthenticationForm):
    pass


def _choice(label, choices, help_text=""):
    return forms.TypedChoiceField(
        label=label,
        choices=choices,
        coerce=int,
        help_text=help_text,
    )


YES_NO = [(0, "No"), (1, "Yes")]


class PredictionForm(StyledFormMixin, forms.Form):
    """The 13 health parameters using the UCI Cleveland dataset coding."""

    # --- Personal details
    age = forms.IntegerField(
        label="Age (years)",
        min_value=1,
        max_value=120,
    )

    sex = _choice(
        "Sex",
        [
            (0, "Female"),
            (1, "Male"),
        ],
    )

    # --- Symptoms
    # UCI Cleveland dataset: cp = 1, 2, 3, 4
    cp = _choice(
        "Chest pain type",
        [
            (1, "1 - Typical angina"),
            (2, "2 - Atypical angina"),
            (3, "3 - Non-anginal pain"),
            (4, "4 - Asymptomatic"),
        ],
        "Code of the 'cp' column",
    )

    exang = _choice(
        "Exercise induced angina",
        YES_NO,
    )

    # --- Vitals and blood tests
    trestbps = forms.IntegerField(
        label="Resting blood pressure (mm Hg)",
        min_value=80,
        max_value=250,
    )

    chol = forms.IntegerField(
        label="Serum cholesterol (mg/dl)",
        min_value=100,
        max_value=600,
    )

    fbs = _choice(
        "Fasting blood sugar above 120 mg/dl",
        YES_NO,
    )

    thalach = forms.IntegerField(
        label="Maximum heart rate achieved (bpm)",
        min_value=60,
        max_value=250,
    )

    # --- ECG and other tests
    restecg = _choice(
        "Resting ECG result",
        [
            (0, "0 - Normal"),
            (1, "1 - ST-T wave abnormality"),
            (2, "2 - Left ventricular hypertrophy"),
        ],
    )

    oldpeak = forms.FloatField(
        label="ST depression induced by exercise",
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(
            attrs={"step": "0.1"}
        ),
    )

    # UCI Cleveland dataset: slope = 1, 2, 3
    slope = _choice(
        "Slope of the peak exercise ST segment",
        [
            (1, "1 - Upsloping"),
            (2, "2 - Flat"),
            (3, "3 - Downsloping"),
        ],
        "Code of the 'slope' column",
    )

    # UCI Cleveland dataset: ca = 0, 1, 2, 3
    ca = _choice(
        "Major vessels coloured by fluoroscopy",
        [
            (0, "0"),
            (1, "1"),
            (2, "2"),
            (3, "3"),
        ],
        "Number of major vessels (0-3)",
    )

    # UCI Cleveland dataset uses thal = 3, 6, 7
    thal = _choice(
        "Thal test result",
        [
            (3, "3 - Normal"),
            (6, "6 - Fixed defect"),
            (7, "7 - Reversible defect"),
        ],
        "Code of the 'thal' column",
    )

    GROUPS = [
        ("Personal details", ["age", "sex"]),
        ("Symptoms", ["cp", "exang"]),
        (
            "Vitals and blood tests",
            ["trestbps", "chol", "fbs", "thalach"],
        ),
        (
            "ECG and other tests",
            ["restecg", "oldpeak", "slope", "ca", "thal"],
        ),
    ]

    def grouped(self):
        """Fields arranged in sections for the template."""
        return [
            (title, [self[name] for name in names])
            for title, names in self.GROUPS
        ]


def describe(record):
    """List of (label, readable value) pairs for a saved PredictionRecord."""

    form = PredictionForm()
    rows = []

    for name in FEATURES:
        field = form.fields[name]
        value = getattr(record, name)

        if isinstance(field, forms.TypedChoiceField):
            value = dict(field.choices).get(value, value)

        rows.append((field.label, value))

    return rows