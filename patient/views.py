
from django.views.generic import CreateView, FormView, TemplateView, UpdateView, DetailView, View, ListView, DeleteView
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
import numpy as np
import joblib
import os
from django.http import Http404
from .forms import  *
from .models import  *
from django.shortcuts import get_object_or_404
from django.urls import reverse

class PatientDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "patient/patient_dashboard.html"
    login_url = 'login'
    redirect_field_name = 'next'



class SinglePatientListView(LoginRequiredMixin, ListView):
    model = PatientInfo
    template_name = "patient/patient_list.html" 
    context_object_name = "patients"
    ordering = ['-created_at'] 
    def get_queryset(self):
        return PatientInfo.objects.filter(user=self.request.user)


"""
    Load Model, Scaler, LabelEncoders, and Feature Order

"""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "kidney_disease_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")
LABEL_ENCODERS_PATH = os.path.join(BASE_DIR, "label_encoders.pkl")
FEATURE_ORDER_PATH = os.path.join(BASE_DIR, "feature_order.pkl")

# Global variables
model, scaler, label_encoders, feature_order = None, None, None, None

if all(os.path.exists(path) for path in [MODEL_PATH, SCALER_PATH, LABEL_ENCODERS_PATH, FEATURE_ORDER_PATH]):
    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        label_encoders = joblib.load(LABEL_ENCODERS_PATH)
        feature_order = joblib.load(FEATURE_ORDER_PATH)  
        print("✅ Model, Scaler, LabelEncoders, and Feature Order loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model, scaler, label encoders, or feature order: {e}")
        model, scaler, label_encoders, feature_order = None, None, None, None
else:
    print("⚠️ Model, Scaler, LabelEncoders, or Feature Order file not found!")


# Prediction View
class PredictKidneyDiseaseView(FormView):
    template_name = "patient/predict.html"
    form_class = PatientForm

    def form_valid(self, form):
        user = self.request.user

        if not hasattr(user, "patient_info"):
            raise ValueError("No PatientInfo profile found for the logged-in user.")

        patient_info = user.patient_info

        if not all([model, scaler, label_encoders, feature_order]):
            raise ValueError("Model, scaler, label encoders, or feature order not loaded.")

        data = form.cleaned_data
        categorical_fields = ['rbc', 'pc', 'pcc', 'ba', 'htn', 'dm', 'cad', 'appet', 'pe', 'ane']

        for field in categorical_fields:
            if field in label_encoders:
                try:
                    data[field] = label_encoders[field].transform([data[field]])[0]
                except ValueError:
                    data[field] = 0  # Default for unknown labels

        try:
            input_data = [data[feature] for feature in feature_order]
        except KeyError as e:
            raise KeyError(f"Missing feature in input data: {e}")

        input_data = np.array(input_data).reshape(1, -1)

        if input_data.shape[1] != len(feature_order):
            raise ValueError(f"Feature count mismatch: Expected {len(feature_order)}, got {input_data.shape[1]}")

        scaled_data = scaler.transform(input_data)
        prediction = model.predict(scaled_data)[0]

        patient = Patient.objects.create(
            patient_info=patient_info,
            **form.cleaned_data,
            prediction="CKD" if prediction == 1 else "Not CKD"
        )

        self.object = patient  # Store for redirection

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("patient:predict_result", kwargs={"pk": self.object.pk})


# Prediction Result View
class PredictResultView(DetailView):
    model = Patient
    template_name = "patient/result.html"
    context_object_name = "patient"

    
# Prediction History View
class PredictionHistoryView(ListView):
    model = Patient
    template_name = "patient/history.html"
    context_object_name = "predictions"

    def get_queryset(self):
        patient_id = self.kwargs.get("patient_id")
        if patient_id:
            return Patient.objects.filter(patient_info_id=patient_id).order_by('-created_at')
        return Patient.objects.none()
    

# 📌 List View - Shows All Patients with Diet Plans
class PatientDietRecommendationView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = "patient/diet_recommendation_list.html"
    context_object_name = "patients"

    def get_queryset(self):
        user = self.request.user

        # Ensure the logged-in user has a PatientInfo profile
        if not hasattr(user, "patient_info"):
            return Patient.objects.none()  # No patient records if no profile exists

        return Patient.objects.filter(patient_info=user.patient_info).order_by('-created_at')
    
# 📌 Detail View - Shows Diet Plan for a Specific Patient
class DietRecommendationsView(DetailView):
    model = Patient
    template_name = "patient/diet_recommendation_detail.html"
    context_object_name = "patient"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["diet"] = DietRecommendation.objects.filter(patient=self.object).first()
        return context

    

class AppointmentListView(ListView):
    model = Appointment
    template_name = "patient/appointment_list.html"
    context_object_name = "appointments"




# Calorie Count - List View
class CalorieListView(ListView):
    model = CalorieRecord
    template_name = "calories/calorie_list.html"
    context_object_name = "calories"

    def get_queryset(self):
        patient_id = self.kwargs.get("patient_id")
        return CalorieRecord.objects.filter(patient_id=patient_id).order_by("-date")


# Calorie Create View
class CalorieCreateView(CreateView):
    model = CalorieRecord
    template_name = "calories/calorie_form.html"
    fields = ["intake", "burnt"]
    
    def form_valid(self, form):
        patient_id = self.kwargs.get("patient_id")
        form.instance.patient = get_object_or_404(Patient, id=patient_id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("calorie_list", kwargs={"patient_id": self.object.patient.id})

# Soul Stretch Views
class SoulStretchListView(ListView):
    model = SoulStretch
    template_name = "calories/soul_stretch.html"
    context_object_name = "stretches"

class SoulStretchCreateView(CreateView):
    model = SoulStretch
    form_class = SoulStretchForm
    template_name = "calories/soul_stretch_form.html"
    success_url = reverse_lazy("soul_stretch")

# Sweat Spot Views
class SweatSpotListView(ListView):
    model = SweatSpot
    template_name = "calories/sweat_spot.html"
    context_object_name = "workouts"

class SweatSpotCreateView(CreateView):
    model = SweatSpot
    form_class = SweatSpotForm
    template_name = "calories/sweat_spot_form.html"
    success_url = reverse_lazy("sweat_spot")


# Calorie Count - List View
class CalorieCreateView(LoginRequiredMixin, CreateView):
    model = CalorieRecord
    form_class = CalorieRecordForm
    template_name = 'calories/calorie_form.html'
    context_object_name = 'form'
    success_url = reverse_lazy("patient:calorie_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the logged-in user to the form
        return context

    def form_valid(self, form):
        # Set the patient field to the logged-in user's patient
        user = self.request.user
        patient = get_object_or_404(CustomUser, patient_info__user=user)

        # Set the patient in the form instance before saving
        form.instance.patient = patient

        return super().form_valid(form)


class CalorieListView(LoginRequiredMixin, ListView):
    model = CalorieRecord
    template_name = 'calories/calorie_list.html'
    context_object_name = 'calorie_records'

    def get_queryset(self):
        # Filter the calorie records based on the logged-in user's patient
        return CalorieRecord.objects.filter(patient=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Prepare data for the chart
        calorie_records = self.get_queryset()
        dates = [record.date.strftime('%Y-%m-%d') for record in calorie_records]
        intake = [record.intake for record in calorie_records]
        burnt = [record.burnt for record in calorie_records]
        
        # Add the chart data to the context
        context['dates'] = dates
        context['intake'] = intake
        context['burnt'] = burnt
        
        return context



