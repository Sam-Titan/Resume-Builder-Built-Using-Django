from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.loginpage, name='login'),
    path('logout', views.logoutpage, name='logout'),
    path('register', views.registerPage, name='register'),
    path('resume/<int:resume_id>/', views.resume, name="resume"),
    path('resume-creation', views.createresume, name="resume-creation"),
    path('resume-update/<int:pk>/', views.updateresume, name="resume-update"),
    path('resume-delete/<int:pk>/', views.deleteresume, name="resume-delete"),
    path('resume/<int:pk>/pdf/', views.generate_resume_pdf, name='resume_pdf'),
    path('resume-ats/<int:pk>/', views.generate_ats, name='resume-ats'),
    path('resume-llm/<int:pk>/', views.generate_llm_response, name="resume-llm"),
]
