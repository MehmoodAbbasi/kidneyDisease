from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import * 

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a unique username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control password-field',
            'placeholder': 'Create a strong password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control password-field',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'role')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']

class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# CKD Prediction Form
# CKD Prediction Form
class PatientForm(forms.ModelForm):
    patient_info = forms.ModelChoiceField(
        queryset=PatientInfo.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'patient-info-select'}),
        label="Select Patient"
    )
    class Meta:
        model = Patient
        fields = [
            'patient_info', 'age', 'bp', 'sg', 'al', 'su', 'rbc', 'pc', 'pcc', 'ba', 'bgr', 'bu', 'sc', 
            'sod', 'pot', 'hemo', 'pcv', 'wc', 'rc', 'htn', 'dm', 'cad', 'appet', 'pe', 'ane'
        ]
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'bp': forms.NumberInput(attrs={'class': 'form-control'}),
            'sg': forms.NumberInput(attrs={'class': 'form-control'}),
            'al': forms.NumberInput(attrs={'class': 'form-control'}),
            'su': forms.NumberInput(attrs={'class': 'form-control'}),
            'rbc': forms.Select(attrs={'class': 'form-control'}, choices=[('normal', 'Normal'), ('abnormal', 'Abnormal')]),
            'pc': forms.Select(attrs={'class': 'form-control'}, choices=[('normal', 'Normal'), ('abnormal', 'Abnormal')]),
            'pcc': forms.Select(attrs={'class': 'form-control'}, choices=[('present', 'Present'), ('notpresent', 'Not Present')]),
            'ba': forms.Select(attrs={'class': 'form-control'}, choices=[('present', 'Present'), ('notpresent', 'Not Present')]),
            'bgr': forms.NumberInput(attrs={'class': 'form-control'}),
            'bu': forms.NumberInput(attrs={'class': 'form-control'}),
            'sc': forms.NumberInput(attrs={'class': 'form-control'}),
            'sod': forms.NumberInput(attrs={'class': 'form-control'}),
            'pot': forms.NumberInput(attrs={'class': 'form-control'}),
            'hemo': forms.NumberInput(attrs={'class': 'form-control'}),
            'pcv': forms.NumberInput(attrs={'class': 'form-control'}),
            'wc': forms.NumberInput(attrs={'class': 'form-control'}),
            'rc': forms.NumberInput(attrs={'class': 'form-control'}),
            'htn': forms.Select(attrs={'class': 'form-control'}, choices=[('yes', 'Yes'), ('no', 'No')]),
            'dm': forms.Select(attrs={'class': 'form-control'}, choices=[('yes', 'Yes'), ('no', 'No')]),
            'cad': forms.Select(attrs={'class': 'form-control'}, choices=[('yes', 'Yes'), ('no', 'No')]),
            'appet': forms.Select(attrs={'class': 'form-control'}, choices=[('good', 'Good'), ('poor', 'Poor')]),
            'pe': forms.Select(attrs={'class': 'form-control'}, choices=[('yes', 'Yes'), ('no', 'No')]),
            'ane': forms.Select(attrs={'class': 'form-control'}, choices=[('yes', 'Yes'), ('no', 'No')]),
        }



class PatientDetailForm(forms.ModelForm):
    class Meta:
        model = PatientInfo
        fields = ["name", "father_name", "age", "address"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter patient name"}),
            "father_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter father’s name"}),
            "age": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter age"}),
            "address": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter address", "rows": 3}),
        }


    
class DietRecommendationForm(forms.ModelForm):
    class Meta:
        model = DietRecommendation
        fields = ['diet_type', 'cuisine_style', 'additional_notes', 'recommended_meals']
        widgets = {
            'diet_type': forms.Select(attrs={'class': 'form-control'}),
            'cuisine_style': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferred cuisine style'}),
            'additional_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional preferences'}),
            'recommended_meals': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Recommended meals...'}),
        }

class AppointmentForm(forms.ModelForm):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), empty_label="Select Patient", widget=forms.Select(attrs={'class': 'form-control'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    consultation_type = forms.ChoiceField(choices=Appointment.CONSULTATION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=Appointment.STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Appointment
        fields = ['patient', 'date', 'time', 'consultation_type', 'status']


# Enhanced Soul Stretch Form (Yoga & Breathing)
class SoulStretchForm(forms.ModelForm):
    class Meta:
        model = SoulStretch
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter yoga/stretch title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Describe the yoga/stretch benefits and steps"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title

# Enhanced Sweat Spot Form (Workout Guidelines)
class SweatSpotForm(forms.ModelForm):
    class Meta:
        model = SweatSpot
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter workout title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Describe the workout guidelines"}),
        }

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) < 10:
            raise forms.ValidationError("Description must be at least 10 characters long.")
        return description