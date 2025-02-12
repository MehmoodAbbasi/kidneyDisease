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
from django.db.models import Sum
import json
from django.db.models import Count
from .forms import  *
from .models import  *
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin

class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomUserLoginForm
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        return self.success_url

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    login_url = 'login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Cards Data
        context["total_patients"] = Patient.objects.count()
        context["total_appointments"] = Appointment.objects.count()
        context["ckd_cases"] = Patient.objects.filter(prediction="CKD").count()
        context["total_diets"] = DietRecommendation.objects.count()

        # Charts Data
        age_groups = {"0-20": (0, 20), "21-40": (21, 40), "41-60": (41, 60), "61+": (61, 100)}
        age_data = {label: Patient.objects.filter(age__range=range).count() for label, range in age_groups.items()}
        context["age_labels"] = json.dumps(list(age_data.keys()))
        context["age_values"] = json.dumps(list(age_data.values()))

        prediction_data = Patient.objects.values("prediction").annotate(count=Count("prediction"))
        context["prediction_labels"] = json.dumps([entry["prediction"] for entry in prediction_data])
        context["prediction_values"] = json.dumps([entry["count"] for entry in prediction_data])

        appointment_data = Appointment.objects.values("status").annotate(count=Count("status"))
        context["appointment_labels"] = json.dumps([entry["status"] for entry in appointment_data])
        context["appointment_values"] = json.dumps([entry["count"] for entry in appointment_data])

        diet_data = DietRecommendation.objects.values("diet_type").annotate(count=Count("diet_type"))
        context["diet_labels"] = json.dumps([entry["diet_type"] for entry in diet_data])
        context["diet_values"] = json.dumps([entry["count"] for entry in diet_data])

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUpdateForm
    template_name = 'profile_update.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return self.request.user

class PatientCreateView(CreateView):
    model = PatientInfo
    form_class = PatientDetailForm
    template_name = "add_patient.html"
    success_url = reverse_lazy("patient_list")

class PatientListView(ListView):
    model = PatientInfo
    template_name = "patient_list.html" 
    context_object_name = "patients"
    ordering = ['-created_at'] 


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
        feature_order = joblib.load(FEATURE_ORDER_PATH)  # Ensure correct feature order
        print("✅ Model, Scaler, LabelEncoders, and Feature Order loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model, scaler, label encoders, or feature order: {e}")
        model, scaler, label_encoders, feature_order = None, None, None, None
else:
    print("⚠️ Model, Scaler, LabelEncoders, or Feature Order file not found!")


# Prediction View
class PredictKidneyDiseaseView(FormView):
    template_name = "predict.html"
    form_class = PatientForm

    def form_valid(self, form):
        if not all([model, scaler, label_encoders, feature_order]):
            raise ValueError("Model, scaler, label encoders, or feature order not loaded. Please check the saved files.")

        # Get cleaned data from form
        data = form.cleaned_data

        # Define categorical fields that need encoding
        categorical_fields = ['rbc', 'pc', 'pcc', 'ba', 'htn', 'dm', 'cad', 'appet', 'pe', 'ane']

        # Encode categorical features safely
        for field in categorical_fields:
            if field in label_encoders:
                try:
                    data[field] = label_encoders[field].transform([data[field]])[0]
                except ValueError:
                    data[field] = 0  # Assign default value for unknown labels

        # Ensure correct feature order
        try:
            input_data = [data[feature] for feature in feature_order]
        except KeyError as e:
            raise KeyError(f"Missing feature in input data: {e}")

        input_data = np.array(input_data).reshape(1, -1)

        # Validate feature count
        if input_data.shape[1] != len(feature_order):
            raise ValueError(f"Feature count mismatch: Expected {len(feature_order)}, but got {input_data.shape[1]}")

        # Scale the input
        scaled_data = scaler.transform(input_data)

        # Make prediction
        prediction = model.predict(scaled_data)[0]

        # Save patient record with prediction
        patient = Patient.objects.create(
            **form.cleaned_data,
            prediction="CKD" if prediction == 1 else "Not CKD"
        )

        # Store patient object for success URL redirection
        self.object = patient

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("prediction_result", kwargs={"pk": self.object.pk})


# Prediction Result View
class PredictionResultView(DetailView):
    model = Patient
    template_name = "result.html"
    context_object_name = "patient"




# Prediction History View
class PredictionHistoryView(ListView):
    model = Patient
    template_name = "history.html"
    context_object_name = "predictions"

    def get_queryset(self):
        patient_id = self.kwargs.get("patient_id")
        if patient_id:
            return Patient.objects.filter(patient_info_id=patient_id).order_by('-created_at')
        return Patient.objects.none()
    

# 📌 List View - Shows All Patients with Diet Plans
class DietRecommendationListView(ListView):
    model = Patient
    template_name = "diet/diet_recommendation_list.html"
    context_object_name = "patients"

# 📌 Detail View - Shows Diet Plan for a Specific Patient
class DietRecommendationDetailView(DetailView):
    model = Patient
    template_name = "diet/diet_recommendation_detail.html"
    context_object_name = "patient"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["diet"] = DietRecommendation.objects.filter(patient=self.object).first()
        return context

# 📌 Create View - Assign a Diet Plan to a Patient
class DietRecommendationCreateView(SuccessMessageMixin, CreateView):
    model = DietRecommendation
    form_class = DietRecommendationForm
    template_name = "diet/diet_recommendation_form.html"
    success_message = "Diet recommendation created successfully!"

    def form_valid(self, form):
        patient = get_object_or_404(Patient, id=self.kwargs['pk'])
        form.instance.patient = patient
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("diet_recommendation_detail", kwargs={"pk": self.kwargs["pk"]})

# 📌 Update View - Edit an Existing Diet Plan
class DietRecommendationUpdateView(SuccessMessageMixin, UpdateView):
    model = DietRecommendation
    form_class = DietRecommendationForm
    template_name = "diet/diet_recommendation_form.html"
    success_message = "Diet recommendation updated successfully!"

    def get_object(self):
        patient = get_object_or_404(Patient, id=self.kwargs["pk"])
        return get_object_or_404(DietRecommendation, patient=patient)

    def get_success_url(self):
        return reverse_lazy("diet_recommendation_detail", kwargs={"pk": self.kwargs["pk"]})
    

class AppointmentListView(ListView):
    model = Appointment
    template_name = "appointments/appointment_list.html"
    context_object_name = "appointments"

class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/appointment_form.html"
    success_url = reverse_lazy("appointment_list")

class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/appointment_form.html"
    success_url = reverse_lazy("appointment_list")

class AppointmentDeleteView(DeleteView):
    model = Appointment
    template_name = "appointments/appointment_confirm_delete.html"
    success_url = reverse_lazy("appointment_list")



# Calorie Count - List View
# Calorie List View (Filtered by Patient)
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