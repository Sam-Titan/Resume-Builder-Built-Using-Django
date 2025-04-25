from django.forms import ModelForm
from django import forms
from .models import (
    Resume, Contact, Education, Experience, Skill, Project, 
    Award, Interest
)

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['name', 'title', 'summary']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'phone', 'linkedin', 'github']


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school_name', 'degree', 'field_of_study', 'start_year', 'end_year', 'cgpa']
        widgets = {
            'start_year': forms.NumberInput(attrs={'min': 1900, 'max': 2100, 'placeholder': 'YYYY'}),
            'end_year': forms.NumberInput(attrs={'min': 1900, 'max': 2100, 'placeholder': 'YYYY'}),
            'cgpa': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'CGPA'}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company_name', 'role', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'url']

class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ['title']
        # widgets = {
        #     'date_received': forms.DateInput(attrs={'type': 'date'}),
        # }

class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['name']

