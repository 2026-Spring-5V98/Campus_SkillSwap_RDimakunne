from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Skill, Review, Appointment


class RegisterForm(UserCreationForm):
    # UserCreationForm gives us username + password fields; we add email
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap's form-control class to every field automatically
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        # owner is set automatically in the view; created_at is set by the DB
        fields = ['title', 'description', 'category', 'price', 'is_free',
                  'contact_preference', 'availability_status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply correct Bootstrap class based on widget type
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean(self):
        # clean() runs after individual field validation — use it for cross-field rules
        cleaned_data = super().clean()
        is_free = cleaned_data.get('is_free')
        price = cleaned_data.get('price')

        # ⚠️ Common mistake: forgetting to validate that free vs. paid are mutually exclusive
        if not is_free and not price:
            raise forms.ValidationError(
                "Please enter a price, or tick 'Free' if you're offering this at no cost."
            )
        if is_free and price:
            raise forms.ValidationError(
                "A skill cannot be both free and have a price. Leave the price blank if it's free."
            )
        return cleaned_data


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'form-control',
                                             'placeholder': 'Any details or questions for the skill owner...'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
