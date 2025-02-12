from django.contrib import admin
from .models import Patient

class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "patient_info", "age", "bp", "sg", "al", "su", "rbc", "pc", "pcc", "ba", "bgr", "bu", "sc",
        "sod", "pot", "hemo", "pcv", "wc", "rc", "htn", "dm", "cad", "appet", "pe", "ane", "prediction", "created_at"
    )
    list_filter = ("prediction", "htn", "dm", "cad", "ane", "pe")
    search_fields = ("age", "bp", "rbc", "pc", "prediction")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

admin.site.register(Patient, PatientAdmin)