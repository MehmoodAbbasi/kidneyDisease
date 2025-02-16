from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    PatientInfo, Patient, DietRecommendation, Appointment, 
    CalorieRecord, SoulStretch, SweatSpot
)
# Register your models here.

# Patient Info Admin
@admin.register(PatientInfo)
class PatientInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'father_name', 'age', 'created_at')
    search_fields = ('name', 'father_name')
    list_filter = ('age', 'created_at')
    ordering = ('-created_at',)


# Inline Diet Recommendation for Patient
class DietRecommendationInline(admin.StackedInline):
    model = DietRecommendation
    extra = 0


# Inline Appointments for Patient
class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 0
    fields = ('date', 'time', 'consultation_type', 'status')


# Patient Admin with inlines
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_info', 'prediction', 'created_at')
    search_fields = ('patient_info__name', 'prediction')
    list_filter = ('prediction', 'created_at')
    ordering = ('-created_at',)
    inlines = [DietRecommendationInline, AppointmentInline]


# Diet Recommendation Admin
@admin.register(DietRecommendation)
class DietRecommendationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'diet_type', 'cuisine_style', 'created_at')
    search_fields = ('patient__patient_info__name',)
    list_filter = ('diet_type', 'created_at')


# Appointment Admin
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'consultation_type', 'date', 'time', 'status')
    search_fields = ('patient__patient_info__name', 'consultation_type')
    list_filter = ('status', 'consultation_type', 'date')
    ordering = ('-date', '-time')


# Calorie Record Admin
@admin.register(CalorieRecord)
class CalorieRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'intake', 'burnt')
    search_fields = ('patient__patient_info__name',)
    list_filter = ('date',)


# Yoga & Breathing Exercises Admin
@admin.register(SoulStretch)
class SoulStretchAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


# Workout Guidelines Admin
@admin.register(SweatSpot)
class SweatSpotAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


# Register Custom User separately


# Admin panel customization
admin.site.site_header = "CKD Health Advisor Admin"
admin.site.site_title = "CKD Admin Panel"
admin.site.index_title = "Welcome to CKD Health Advisor"