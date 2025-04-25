from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resumes", null=True)
    name = models.CharField(max_length=200)  # Removed default=user.name (invalid)
    title = models.CharField(max_length=200)
    summary = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Contact(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name="contact")
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.email

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="education")
    school_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(blank=True, null=True)
    cgpa = models.DecimalField(
        max_digits=4,  # Allows CGPA like 9.99 or 10.0
        decimal_places=2,  
        blank=True, 
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]  # Adjust based on your grading system
    )

    def __str__(self):
        cgpa_display = f", CGPA: {self.cgpa}" if self.cgpa is not None else ""
        return f"{self.degree} - {self.school_name} ({self.start_year} - {self.end_year if self.end_year else 'Present'}){cgpa_display}"


class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="experience")
    company_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.role} at {self.company_name}"

class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Award(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="awards")
    title = models.CharField(max_length=255)
    # description = models.TextField(blank=True, null=True)
    # date_received = models.DateField()

    def __str__(self):
        return self.title

class Interest(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="interests")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
