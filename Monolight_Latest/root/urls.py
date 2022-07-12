from django.urls import path
from . import views

urlpatterns = [
    path('all_profile/', views.all_profile, name="all_profile"),
    path('all_attendance/', views.all_attendance, name="all_attendance"),
    path('all_graphs/', views.all_graphs, name="all_graphs"),
    path('requests/', views.requests, name="requests"),
] 