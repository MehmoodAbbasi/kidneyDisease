from django.urls import path
from .views import *
app_name = 'patient'
urlpatterns = [
    path('', PatientDashboardView.as_view(), name='patient_dashboard'),

    path('patient/', SinglePatientListView.as_view(), name='patient'),
    path("predicts/", PredictKidneyDiseaseView.as_view(), name="patient_perdict"),
    path("result/<int:pk>/", PredictResultView.as_view(), name="predict_result"),
    path('diet-plan/', PatientDietRecommendationView.as_view(), name='patinet_diet'),
    path("patient/<int:patient_id>/history/", PredictionHistoryView.as_view(), name="patient_record"),
    path('diet-recomends/<int:pk>/', DietRecommendationsView.as_view(), name='diet_recommendations'),

    path('appointments/', AppointmentListView.as_view(), name='appointment_list'),


    path("patients/<int:patient_id>/calories/", CalorieListView.as_view(), name="calorie_list"),
    path("patients/<int:patient_id>/calories/add/", CalorieCreateView.as_view(), name="calorie_add"),
    
    path("soul-stretch/", SoulStretchListView.as_view(), name="soul_stretch"),
    path("soul-stretch/add/", SoulStretchCreateView.as_view(), name="add_soul_stretch"),
    
    path("sweat-spot/", SweatSpotListView.as_view(), name="sweat_spot"),
    path("sweat-spot/add/", SweatSpotCreateView.as_view(), name="add_sweat_spot"),


]