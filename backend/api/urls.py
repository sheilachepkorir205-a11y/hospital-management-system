from django.urls import path

from . import views
from .auth_views import login_view, logout_view


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('patients/', views.patient_list, name='patient-list'),
    path('patients/register/', views.patient_create, name='patient-create'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient-detail'),
    path('patients/<int:patient_id>/edit/', views.patient_update, name='patient-update'),
    path('doctors/', views.doctor_list, name='doctor-list'),
    path('doctors/add/', views.doctor_create, name='doctor-create'),
    path('doctors/<int:doctor_id>/', views.doctor_detail, name='doctor-detail'),
    path('doctors/<int:doctor_id>/edit/', views.doctor_update, name='doctor-update'),
    path('nurses/', views.nurse_list, name='nurse-list'),
    path('nurses/add/', views.nurse_create, name='nurse-create'),
    path('nurses/<int:nurse_id>/', views.nurse_detail, name='nurse-detail'),
    path('nurses/<int:nurse_id>/edit/', views.nurse_update, name='nurse-update'),
    path('departments/', views.department_list, name='department-list'),
    path('departments/add/', views.department_create, name='department-create'),
    path('departments/<int:department_id>/', views.department_detail, name='department-detail'),
    path('departments/<int:department_id>/edit/', views.department_update, name='department-update'),
    path('insurance-providers/', views.provider_list, name='provider-list'),
    path('insurance-providers/add/', views.provider_create, name='provider-create'),
    path('insurance-providers/<int:provider_id>/', views.provider_detail, name='provider-detail'),
    path('insurance-providers/<int:provider_id>/edit/', views.provider_update, name='provider-update'),
]