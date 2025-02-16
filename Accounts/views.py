from django.views.generic import CreateView, TemplateView, UpdateView,  View
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
import json
from django.db.models import Count
from .forms import  *
from .models import  *
from patient.models import *

class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomUserLoginForm

    def get_success_url(self):
        user = self.request.user
        if user.role == 'patient':
            return reverse_lazy('patient_dashboard')
        return reverse_lazy('dashboard')

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

