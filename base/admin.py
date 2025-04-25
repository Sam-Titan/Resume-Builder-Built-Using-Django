from django.contrib import admin
from .models import (
    Resume, Contact, Education, Experience, Skill, Project, 
    Award, Interest
)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'updated', 'created')
    search_fields = ('name', 'title')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('resume', 'email', 'phone', 'linkedin')
    search_fields = ('email', 'linkedin')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'field_of_study', 'school_name', 'start_year', 'end_year', 'cgpa')
    search_fields = ('degree', 'school_name')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company_name', 'start_date', 'end_date')
    search_fields = ('role', 'company_name')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    search_fields = ('title',)

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
