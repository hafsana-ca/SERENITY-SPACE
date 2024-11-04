from django.urls import path
from DoctorApp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("doctor_home/",views.doctor_home,name="doctor_home"),
    path("doctor_register/",views.doctor_register,name="doctor_register"),
    path("dr_register_page/",views.dr_register_page,name="dr_register_page"),
    path("dr_login_page/",views.dr_login_page,name="dr_login_page"),
    path("dr_login/",views.dr_login,name="dr_login"),
    path("dr_logout/",views.dr_logout,name="dr_logout"),
    path("doctor_profile/<int:doctor_id>/",views.doctor_profile,name="doctor_profile"),
    path('add_event/', views.add_event, name='add_event'),
    path('doctor_events/', views.doctor_events, name='doctor_events'),  # For listing events later
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('update_event/<int:event_id>/', views.update_event, name='update_event'),
    path('delete_event/<int:event_id>', views.delete_event, name='delete_event'),
    path('view_registered_users/<int:event_id>/', views.view_registered_users, name='view_registered_users'),
    path('doctor_appointment/', views.doctor_appointment, name='doctor_appointment'),
    path('view_appointments/', views.view_appointments, name='view_appointments'),
]


