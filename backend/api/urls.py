"""
URL patterns for the API app.

Routes:
- POST /api/upload/       -> upload CSV and get summary
- GET  /api/history/      -> get last 5 datasets
- GET  /api/report/<id>/  -> generate PDF report
- POST /api/auth/login/   -> get auth token
"""

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('history/', views.get_history, name='get_history'),
    path('report/<int:pk>/', views.generate_report, name='generate_report'),
    path('auth/login/', views.login_view, name='login'),
]
