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
    path("workouts/", WorkoutListView.as_view(), name="patient_workouts"),
    path("youga-breathing/", YougaListView.as_view(), name="patient_youga"),



    path('calories/', CalorieCreateView.as_view(), name='calorie_create'),
    path('calorie-list/', CalorieListView.as_view(), name='calorie_list'),



]