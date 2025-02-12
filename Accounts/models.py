import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid
from django.urls import reverse_lazy


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient')
    )
    email = models.EmailField(unique=True)
    user_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username
    

class PatientInfo(models.Model):
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.age} years"

    def get_absolute_url(self):
        return reverse_lazy("patient_list")
    
# CKD Prediction Model
class Patient(models.Model):
    patient_info = models.ForeignKey(PatientInfo, on_delete=models.CASCADE, related_name="patients")
    age = models.FloatField()
    bp = models.FloatField(verbose_name="Blood Pressure")
    sg = models.FloatField(verbose_name="Specific Gravity")
    al = models.FloatField(verbose_name="Albumin")
    su = models.FloatField(verbose_name="Sugar")
    rbc = models.CharField(max_length=10, verbose_name="Red Blood Cells")
    pc = models.CharField(max_length=10, verbose_name="Pus Cells")
    pcc = models.CharField(max_length=10, verbose_name="Pus Cell Clumps")
    ba = models.CharField(max_length=10, verbose_name="Bacteria")
    bgr = models.FloatField(verbose_name="Blood Glucose Random")
    bu = models.FloatField(verbose_name="Blood Urea")
    sc = models.FloatField(verbose_name="Serum Creatinine")
    sod = models.FloatField(verbose_name="Sodium")
    pot = models.FloatField(verbose_name="Potassium")
    hemo = models.FloatField(verbose_name="Hemoglobin")
    pcv = models.FloatField(verbose_name="Packed Cell Volume")
    wc = models.FloatField(verbose_name="White Blood Cell Count")
    rc = models.FloatField(verbose_name="Red Blood Cell Count")
    htn = models.CharField(max_length=3, verbose_name="Hypertension")
    dm = models.CharField(max_length=3, verbose_name="Diabetes Mellitus")
    cad = models.CharField(max_length=3, verbose_name="Coronary Artery Disease")
    appet = models.CharField(max_length=10, verbose_name="Appetite")
    pe = models.CharField(max_length=3, verbose_name="Pedal Edema")
    ane = models.CharField(max_length=3, verbose_name="Anemia")
    prediction = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse_lazy("prediction_result", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.patient_info.name} - {self.prediction}"


class DietRecommendation(models.Model):
    DIET_CHOICES = [
        ('Vegetarian', 'Vegetarian'),
        ('Non-Vegetarian', 'Non-Vegetarian'),
        ('Vegan', 'Vegan'),
    ]
    
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name="diet")
    diet_type = models.CharField(max_length=20, choices=DIET_CHOICES)
    cuisine_style = models.CharField(max_length=100, blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)
    recommended_meals = models.TextField(help_text="List recommended meals")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diet for {self.patient.patient_info}"
    

class Appointment(models.Model):
    CONSULTATION_CHOICES = [
        ('Doctor', 'Doctor'),
        ('Health Counselor', 'Health Counselor'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Rescheduled', 'Rescheduled'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    date = models.DateField()
    time = models.TimeField()
    consultation_type = models.CharField(max_length=20, choices=CONSULTATION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.patient_info} - {self.consultation_type} on {self.date} at {self.time}"
    

# Calorie Count Model (Linked to Patient)
class CalorieRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="calories")
    date = models.DateField(auto_now_add=True)
    intake = models.PositiveIntegerField(help_text="Calories consumed")
    burnt = models.PositiveIntegerField(help_text="Calories burnt")
    
    def __str__(self):
        return f"{self.patient.patient_info.name} - {self.date} | Intake: {self.intake} | Burnt: {self.burnt}"

# Yoga & Breathing Exercises
class SoulStretch(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="yoga_images/", blank=True, null=True)
    video = models.FileField(upload_to="yoga_videos/", blank=True, null=True)
    
    def __str__(self):
        return self.title

# Workout Guidelines
class SweatSpot(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="workout_images/", blank=True, null=True)
    video = models.FileField(upload_to="workout_videos/", blank=True, null=True)
    
    def __str__(self):
        return self.title