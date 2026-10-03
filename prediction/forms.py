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
            raise forms.ValidationError("An account with this email already exists.")
        return email


class LoginForm(StyledFormMixin, AuthenticationForm):
    pass


def _choice(label, choices, help_text=""):
    return forms.TypedChoiceField(label=label, choices=choices, coerce=int, help_text=help_text)


YES_NO = [(0, "No"), (1, "Yes")]


class PredictionForm(StyledFormMixin, forms.Form):
    """The 13 health parameters. Codes follow the columns of dataset/heart.csv."""

    # --- Personal details
    age = forms.IntegerField(label="Age (years)", min_value=1, max_value=120)
    sex = _choice("Sex", [(0, "Female"), (1, "Male")])

    # --- Symptoms
    cp = _choice("Chest pain type", [
        (0, "0 - Typical angina"),
        (1, "1 - Atypical angina"),
        (2, "2 - Non-anginal pain"),
        (3, "3 - Asymptomatic"),
    ], "Code of the 'cp' column")
    exang = _choice("Exercise induced angina", YES_NO)

    # --- Vitals and blood tests
    trestbps = forms.IntegerField(label="Resting blood pressure (mm Hg)", min_value=80, max_value=250)
    chol = forms.IntegerField(label="Serum cholesterol (mg/dl)", min_value=100, max_value=600)
    fbs = _choice("Fasting blood sugar above 120 mg/dl", YES_NO)
    thalach = forms.IntegerField(label="Maximum heart rate achieved (bpm)", min_value=60, max_value=250)

    # --- ECG and other tests
    restecg = _choice("Resting ECG result", [
        (0, "0 - Normal"),
        (1, "1 - ST-T wave abnormality"),
        (2, "2 - Left ventricular hypertrophy"),
    ])
    oldpeak = forms.FloatField(
        label="ST depression induced by exercise", min_value=0, max_value=10,
        widget=forms.NumberInput(attrs={"step": "0.1"}),
    )
    slope = _choice("Slope of the peak exercise ST segment", [
        (0, "0 - Upsloping"),
        (1, "1 - Flat"),
        (2, "2 - Downsloping"),
    ])
    ca = _choice("Major vessels coloured by fluoroscopy", [(i, str(i)) for i in range(5)])
    thal = _choice("Thal test result", [
        (0, "0 - Unknown"),
        (1, "1 - Fixed defect"),
        (2, "2 - Normal"),
        (3, "3 - Reversible defect"),
    ], "Use the same coding as the 'thal' column of your heart.csv")

    GROUPS = [
        ("Personal details", ["age", "sex"]),
        ("Symptoms", ["cp", "exang"]),
        ("Vitals and blood tests", ["trestbps", "chol", "fbs", "thalach"]),
        ("ECG and other tests", ["restecg", "oldpeak", "slope", "ca", "thal"]),
    ]

    def grouped(self):
        """Fields arranged in sections for the template."""
        return [(title, [self[name] for name in names]) for title, names in self.GROUPS]


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
