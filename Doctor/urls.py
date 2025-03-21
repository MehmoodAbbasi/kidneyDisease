from django.urls import path
from .views import *


urlpatterns = [
    path("predict/", PredictKidneyDiseaseView.as_view(), name="predict"),
    path("results/<int:pk>/", PredictionResultView.as_view(), name="prediction_result"),
    path("patient/<int:patient_id>/history/", PredictionHistoryView.as_view(), name="patient_history"),
    path('patients/', PatientListView.as_view(), name='patient_list'),
    path("patients/add/", PatientCreateView.as_view(), name="add_patient"),
    path('diet/', DietRecommendationListView.as_view(), name='diet_recommendation_list'),
    path('diet/<int:pk>/', DietRecommendationDetailView.as_view(), name='diet_recommendation_detail'),
    path('diet/<int:pk>/create/', DietRecommendationCreateView.as_view(), name='diet_recommendation_create'),
    path('diet/<int:pk>/update/', DietRecommendationUpdateView.as_view(), name='diet_recommendation_update'),

    path('appointments/', AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/new/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/edit/<int:pk>/', AppointmentUpdateView.as_view(), name='appointment_update'),
    path('appointments/delete/<int:pk>/', AppointmentDeleteView.as_view(), name='appointment_delete'),

    
    path("soul-stretch/", SoulStretchListView.as_view(), name="soul_stretch"),
    path("soul-stretch/add/", SoulStretchCreateView.as_view(), name="add_soul_stretch"),
    
    path("sweat-spot/", SweatSpotListView.as_view(), name="sweat_spot"),
    path("sweat-spot/add/", SweatSpotCreateView.as_view(), name="add_sweat_spot"),




]