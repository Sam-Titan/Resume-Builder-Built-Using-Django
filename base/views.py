from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .models import Resume, Education, Experience, Skill, Project, Award, Interest, Contact
from .forms import ResumeForm, ContactForm,EducationForm, ExperienceForm, SkillForm, ProjectForm, AwardForm, InterestForm
from django.forms import inlineformset_factory
import requests

# Create your views here.


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password")

        # Debugging: Print input values
        print("Username entered:", username)
        print("Password entered:", password)

        # Ensure case-insensitive username lookup
        try:
            user_obj = User.objects.get(username__iexact=username)
            username = user_obj.username  # Get correct case
        except User.DoesNotExist:
            pass

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("Login successful for:", username)
            return redirect('home')
        else:
            print("Authentication failed for:", username)
            messages.error(request, "This username or password is incorrect")

    return render(request, 'base/login_register.html', {'page': 'login'})

def logoutpage(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'base/login_register.html', {'form': form, 'page':'register'})

def home(request):
    q= request.GET.get('q') if request.GET.get('q') !=None else ''
    resumes = Resume.objects.filter(
        Q(title__icontains=q)| 
        Q(summary__icontains=q))
    
    topics = Resume.objects.all()
    context={'resumes':resumes , 'topics':topics}
    return render(request, "base/home.html", context)

def resume(request, resume_id):
    resume = Resume.objects.get(id=resume_id)
    contact = Contact.objects.get(resume_id=resume_id)
    education = resume.education.all()
    experience = resume.experience.all()
    skills = resume.skills.all()
    projects = resume.projects.all()
    award = Award.objects.all()
    interests = Interest.objects.all()
    
    return render(request, 'base/resume_template.html', {
        'resume': resume,
        'contact': contact,
        'education': education,
        'experience': experience,
        'skills': skills,
        'projects': projects,
        'awards': award,
        'interests': interests,
    })

def createresume(request):
    # Define inline formsets
    EducationFormSet = inlineformset_factory(Resume, Education, form=EducationForm, extra=1, can_delete=True)
    ExperienceFormSet = inlineformset_factory(Resume, Experience, form=ExperienceForm, extra=1, can_delete=True)
    SkillFormSet = inlineformset_factory(Resume, Skill, form=SkillForm, extra=1, can_delete=True)
    ProjectFormSet = inlineformset_factory(Resume, Project, form=ProjectForm, extra=1, can_delete=True)
    AwardFormSet = inlineformset_factory(Resume, Award, form=AwardForm, extra=1, can_delete=True)
    InterestFormSet = inlineformset_factory(Resume, Interest, form=InterestForm, extra=1, can_delete=True)

    # Initialize forms
    form = ResumeForm()
    contact_form = ContactForm()
    education_formset = EducationFormSet()
    experience_formset = ExperienceFormSet()
    skill_formset = SkillFormSet()
    project_formset = ProjectFormSet()
    award_formset = AwardFormSet()
    interest_formset = InterestFormSet()

    if request.method == "POST":
        form = ResumeForm(request.POST)
        contact_form = ContactForm(request.POST)
        education_formset = EducationFormSet(request.POST)
        experience_formset = ExperienceFormSet(request.POST)
        skill_formset = SkillFormSet(request.POST)
        project_formset = ProjectFormSet(request.POST)
        award_formset = AwardFormSet(request.POST)
        interest_formset = InterestFormSet(request.POST)
        if form.is_valid() and contact_form.is_valid() and all([
            education_formset.is_valid(), experience_formset.is_valid(),
            skill_formset.is_valid(), project_formset.is_valid(),
            award_formset.is_valid(), 
            interest_formset.is_valid(), 
        ]):
            # Save resume and contact info
            resume = form.save()
            contact = contact_form.save(commit=False)
            contact.resume = resume
            contact.save()

            # Save all related formsets
            for formset in [education_formset, experience_formset, skill_formset, project_formset,
                            award_formset, interest_formset]:
                items = formset.save(commit=False)
                for item in items:
                    item.resume = resume  # Corrected typo
                    item.save()
                formset.save_m2m()  # Save many-to-many data if any

            return redirect('home')

    context = {
        'form': form,
        'contact_form': contact_form,
        'education_formset': education_formset,
        'experience_formset': experience_formset,
        'skill_formset': skill_formset,
        'project_formset': project_formset,
        'award_formset': award_formset,
        'interest_formset': interest_formset,
    }
    return render(request, "base/resume_page.html", context)

def updateresume(request, pk):
    # Get the resume object or return a 404 error if not found
    resume = get_object_or_404(Resume, id=pk)

    # Ensure the resume has a Contact object
    contact, created = Contact.objects.get_or_create(resume=resume)

    # Define formsets
    EducationFormSet = inlineformset_factory(Resume, Education, form=EducationForm, extra=1, can_delete=True)
    ExperienceFormSet = inlineformset_factory(Resume, Experience, form=ExperienceForm, extra=1, can_delete=True)
    SkillFormSet = inlineformset_factory(Resume, Skill, form=SkillForm, extra=1, can_delete=True)
    ProjectFormSet = inlineformset_factory(Resume, Project, form=ProjectForm, extra=1, can_delete=True)
    AwardFormSet = inlineformset_factory(Resume, Award, form=AwardForm, extra=1, can_delete=True)
    InterestFormSet = inlineformset_factory(Resume, Interest, form=InterestForm, extra=1, can_delete=True)

    # Initialize forms
    form = ResumeForm(instance=resume)
    contact_form = ContactForm(instance=contact)
    education_formset = EducationFormSet(instance=resume)
    experience_formset = ExperienceFormSet(instance=resume)
    skill_formset = SkillFormSet(instance=resume)
    project_formset = ProjectFormSet(instance=resume)
    award_formset = AwardFormSet(instance=resume)
    interest_formset = InterestFormSet(instance=resume)

    if request.method == "POST":
        form = ResumeForm(request.POST, instance=resume)
        contact_form = ContactForm(request.POST, instance=contact)
        education_formset = EducationFormSet(request.POST, instance=resume)
        experience_formset = ExperienceFormSet(request.POST, instance=resume)
        skill_formset = SkillFormSet(request.POST, instance=resume)
        project_formset = ProjectFormSet(request.POST, instance=resume)
        award_formset = AwardFormSet(request.POST, instance=resume)
        interest_formset = InterestFormSet(request.POST, instance=resume)

        if form.is_valid() and contact_form.is_valid() and all([
            education_formset.is_valid(), experience_formset.is_valid(),
            skill_formset.is_valid(), project_formset.is_valid(),
        ]):
            # Save the resume and contact forms
            form.save()
            contact_form.save()

            # Save all related formsets
            for formset in [education_formset, experience_formset, skill_formset, project_formset,
                            award_formset, interest_formset]:
                items = formset.save(commit=False)
                for item in items:
                    item.resume = resume
                    item.save()
                formset.save_m2m()  # Save many-to-many data if any

                # Handle deletions
                for item in formset.deleted_objects:
                    item.delete()

            return redirect('home')
        else:
            # Debugging: Print form and formset errors
            print("Form Errors:", form.errors)
            print("Contact Form Errors:", contact_form.errors)
            print("Education Formset Errors:", education_formset.errors)
            print("Experience Formset Errors:", experience_formset.errors)
            print("Skill Formset Errors:", skill_formset.errors)
            print("Project Formset Errors:", project_formset.errors)
            print("Award Formset Errors:", award_formset.errors)
            print("Interest Formset Errors:", interest_formset.errors)

    context = {
        'form': form,
        'contact_form': contact_form,
        'education_formset': education_formset,
        'experience_formset': experience_formset,
        'skill_formset': skill_formset,
        'project_formset': project_formset,
        'award_formset': award_formset,
        'interest_formset': interest_formset,
    }
    return render(request, 'base/resume_page.html', context)



def deleteresume(request,pk):
    resume = Resume.objects.get(id=pk)
    if request.method == "POST":
        resume.delete()
        return redirect('home')
    context={'obj':resume}
    return render(request, 'base/delete.html', context)

import os
import time
import tempfile
from django.http import FileResponse, HttpResponse
from playwright.sync_api import sync_playwright

def generate_resume_pdf(request, pk):
    # ✅ Fetch the correct resume page URL
    resume_url = request.build_absolute_uri(f'/resume/{pk}/')  

    # ✅ Create a temporary file path
    temp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(temp_dir, f'resume_{pk}.pdf')

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(resume_url, wait_until="load")  # ✅ Ensure full page load
        page.pdf(path=pdf_path, format="A4")
        browser.close()

    time.sleep(1)  # ✅ Ensure file is fully written

    if not os.path.exists(pdf_path):
        return HttpResponse("PDF generation failed", status=500)

    # ✅ Open file safely and serve it
    response = FileResponse(open(pdf_path, "rb"), as_attachment=True, filename=f"resume_{pk}.pdf")

    # ✅ Cleanup file after sending response
    try:
        os.remove(pdf_path)
    except PermissionError:
        pass  # Ignore if the file is in use

    return response




import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyCocHWHmtSfflsW8fn8lMaZfmDrj-QhVgo")  # Replace with your actual API key

def generate_llm_response(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    model = genai.GenerativeModel("gemini-2.0-flash")

    # Gather existing data
    experiences = "\n".join([f"{exp.role} at {exp.company_name}: {exp.description}" for exp in resume.experience.all()])
    skills = ", ".join(resume.skills.values_list("name", flat=True))
    projects = "\n".join([f"{proj.title}: {proj.description}" for proj in resume.projects.all()])
    awards = ", ".join(resume.awards.values_list("title", flat=True))
    interests = ", ".join(resume.interests.values_list("name", flat=True))

    # LLM prompt
    prompt = f"""
    Improve the following resume sections. Return only the improved text in a structured format.

    **Resume Summary:** (Make it more generic and personalized based on experience and skills)
    {resume.summary}

    **Experience:** (Rewrite descriptions, keeping them role-specific & compelling without merging entries)
    {experiences}

    **Skills:** (Only spell-check and correct typos)
    {skills}

    **Projects:** (Enhance descriptions, making them detailed & engaging)
    {projects}

    **Awards:** (Only spell-check titles)
    Awards: {awards}

    **Interests:** (Spell-check and refine if needed)
    {interests}

    **Return the improved sections in this format:**
    - Resume Summary: [Updated summary]
    - Experience: [Each job description on a new line]
    - Skills: [Comma-separated list]
    - Projects: [Each project on a new line]
    - Awards: [Updated list]
    - Interests: [Updated list]
    """

    response = model.generate_content(prompt)
    improved_text = response.text.strip()

    # Ensure structured output
    sections = {
        "summary": "",
        "experience": [],
        "skills": [],
        "projects": [],
        "awards": [],
        "interests": []
    }

    current_section = None

    for line in improved_text.split("\n"):
        line = line.strip()

        # Detect section headers
        if line.startswith("- Resume Summary:"):
            current_section = "summary"
            sections["summary"] = line.replace("- Resume Summary:", "").strip()

        elif line.startswith("- Experience:"):
            current_section = "experience"

        elif line.startswith("- Skills:"):
            current_section = "skills"

        elif line.startswith("- Projects:"):
            current_section = "projects"

        elif line.startswith("- Awards:"):
            current_section = "awards"

        elif line.startswith("- Interests:"):
            current_section = "interests"

        # Assign parsed content
        elif current_section == "summary":
            sections["summary"] += " " + line  # Concatenation for multi-line summary

        elif current_section in ["skills", "interests"]:
            sections[current_section].extend([s.strip() for s in line.split(",") if s.strip()])

        elif current_section in ["experience", "projects", "awards"]:
            sections[current_section].append(line)

    # Update resume summary
    resume.summary = sections["summary"]

    # Update Experience Descriptions (Maintains separation)
    experience_entries = list(resume.experience.all())
    for idx, exp_desc in enumerate(sections["experience"]):
        if idx < len(experience_entries):
            experience_entries[idx].description = exp_desc
            experience_entries[idx].save()

    # Spell-check Skills (No new additions, just corrections)
    skill_entries = list(resume.skills.all())
    for idx, skill_name in enumerate(sections["skills"]):
        if idx < len(skill_entries):
            skill_entries[idx].name = skill_name
            skill_entries[idx].save()

    # Update Project Descriptions
    project_entries = list(resume.projects.all())
    for idx, proj_desc in enumerate(sections["projects"]):
        if idx < len(project_entries):
            project_entries[idx].description = proj_desc
            project_entries[idx].save()

    # Spell-check Awards (Ensuring no data loss)
    award_entries = list(resume.awards.all())
    for idx, award_name in enumerate(sections["awards"]):
        if idx < len(award_entries):
            award_entries[idx].title = award_name
            award_entries[idx].save()

    # Spell-check Interests
    interest_entries = list(resume.interests.all())
    for idx, interest_name in enumerate(sections["interests"]):
        if idx < len(interest_entries):
            interest_entries[idx].name = interest_name
            interest_entries[idx].save()

    resume.save()
    
    return redirect('resume', resume_id=resume.pk)



from spellchecker import SpellChecker
import logging
import re
# Set up logging
logger = logging.getLogger(__name__)

# List of common stopwords to filter out
STOPWORDS = set([
    "a", "an", "the", "and", "or", "in", "on", "at", "for", "to", "of", 
    "with", "as", "by", "is", "are", "was", "were", "be", "been", "being"
])

def normalize_text(text):
    """
    Normalizes text by removing punctuation, converting to lowercase, and stripping whitespace.
    """
    if not text:
        return ""
    # Replace hyphens and special characters with spaces
    text = re.sub(r'[^\w\s]', ' ', text.lower()).strip()
    # Normalize multiple spaces into a single space
    text = re.sub(r'\s+', ' ', text)
    return text

def spell_check_text(text, spell=None):
    """
    Spell-checks a given text and ensures no None values cause issues.
    """
    if not text:
        return ""
    
    if spell is None:
        spell = SpellChecker()
    
    words = text.split()
    corrected_words = [spell.correction(word) if spell.correction(word) else word for word in words]
    return " ".join(corrected_words)

def extract_keywords(text, enable_spell_check=False):
    """
    Extracts keywords from a given text, including multi-word keywords.
    """
    if not text:
        return set()
    
    # Normalize text
    text = normalize_text(text)
    
    # Apply spell checking if enabled
    if enable_spell_check:
        spell = SpellChecker()
        text = spell_check_text(text, spell)
    
    # Split into words
    words = text.split()
    
    # Extract single-word and multi-word keywords
    keywords = set()
    for i in range(len(words)):
        # Single-word keyword
        if len(words[i]) > 2 and words[i] not in STOPWORDS:
            keywords.add(words[i])
        # Multi-word keyword (e.g., "rest api")
        if i < len(words) - 1:
            bigram = f"{words[i]} {words[i+1]}"
            if not (words[i] in STOPWORDS and words[i+1] in STOPWORDS):
                keywords.add(bigram)
    
    return keywords

def extract_resume_keywords(resume, enable_spell_check=False):
    """
    Extracts and processes keywords from the resume's structured and unstructured fields.
    """
    try:
        # Fetch all related objects in fewer queries
        skills = list(Skill.objects.filter(resume=resume))
        experiences = list(Experience.objects.filter(resume=resume))
        education_fields = list(Education.objects.filter(resume=resume))
        projects = list(Project.objects.filter(resume=resume))
        awards = list(Award.objects.filter(resume=resume))
        interests = list(Interest.objects.filter(resume=resume))
        
        # Keywords from structured fields
        structured_keywords = set()
        structured_keywords.update(skill.name.lower() for skill in skills if skill.name)
        structured_keywords.update(exp.role.lower() for exp in experiences if exp.role)
        structured_keywords.update(edu.field_of_study.lower() for edu in education_fields if edu.field_of_study)
        structured_keywords.update(proj.title.lower() for proj in projects if proj.title)
        structured_keywords.update(award.title.lower() for award in awards if award.title)
        structured_keywords.update(interest.name.lower() for interest in interests if interest.name)
        
        # Keywords from unstructured fields
        experience_descriptions = " ".join(exp.description for exp in experiences if exp.description)
        project_descriptions = " ".join(proj.description for proj in projects if proj.description)
        resume_summary = resume.summary or ""
        
        # Combine all unstructured text
        unstructured_text = " ".join([experience_descriptions, project_descriptions, resume_summary])
        unstructured_keywords = extract_keywords(unstructured_text, enable_spell_check)
        
        # Combine all keywords
        return structured_keywords | unstructured_keywords
    except Exception as e:
        logger.error(f"Error extracting resume keywords: {e}")
        return set()

def calculate_ats_score(resume, job_keywords, enable_spell_check=True):
    """
    Calculates the ATS score for a resume based on job keywords.
    """
    try:
        # Extract keywords from the resume
        resume_keywords = extract_resume_keywords(resume, enable_spell_check)
        
        # Normalize job keywords
        normalized_job_keywords = {normalize_text(keyword) for keyword in job_keywords}
        
        # Match keywords
        matched_keywords = normalized_job_keywords.intersection(resume_keywords)
        unmatched_keywords = normalized_job_keywords - resume_keywords
        
        # Calculate score
        if not normalized_job_keywords:
            return 0, set(), set(), "No job keywords provided"
        
        score = (len(matched_keywords) / len(normalized_job_keywords)) * 100
        return round(score, 2), matched_keywords, unmatched_keywords, ""
    except Exception as e:
        error_msg = f"Error calculating ATS score: {e}"
        logger.error(error_msg)
        return 0, set(), set(), error_msg

def generate_ats(request, pk):
    """
    View to handle ATS scoring and render the results.
    """
    try:
        resume = get_object_or_404(Resume, id=pk)
        
        # Sample job keywords (can be fetched from a database or user input)
        job_keywords = {"Python", "Django", "Web Development", "Machine Learning", 
                        "REST API", "SQL", "Cloud", "API Development", "Data Analysis"}
        
        # Get spell check preference from request or default to True
        enable_spell_check = request.GET.get('spell_check', 'true').lower() == 'true'
        
        # Calculate ATS score
        score, matched_keywords, unmatched_keywords, error = calculate_ats_score(
            resume, job_keywords, enable_spell_check)
        
        if error:
            return render(request, 'base/error.html', {'error': error})
        
        # Prepare context
        context = {
            'candidate': resume.name,
            'ats_score': score,
            'matched_keywords': matched_keywords,
            'unmatched_keywords': unmatched_keywords,
            'total_keywords': len(matched_keywords) + len(unmatched_keywords),
            'enable_spell_check': enable_spell_check,
            'skills': Skill.objects.filter(resume=resume),
            'experiences': Experience.objects.filter(resume=resume),
            'education': Education.objects.filter(resume=resume),
            'projects': Project.objects.filter(resume=resume),
            'awards': Award.objects.filter(resume=resume),
            'resume_summary': resume.summary,
        }
        
        return render(request, 'base/ats_score.html', context)
    except Exception as e:
        error_msg = f"Error generating ATS score: {e}"
        logger.error(error_msg)
        return render(request, 'base/error.html', {'error': error_msg})
    

# class Blog(BaseModel):
#     title: str
#     age: int

# @app.get('/')
# def index(limit=10, published:bool = True):
#     if published:
#         return f"{limit} Published Blogs"
#     else:
#         return "Nopublished Blogs"
    
# @app.get('/blog/{id}')
# def index(id:int):
#     return f"{id} is the id of the published blog"

# @app.post('/blog')
# def create_blog(request:Blog):
#     return f"{request.title} is of {request.age}"

# @app.get('/resume')
# def getinfo(resume_id:int):
#     print(f"Received resume ID: {resume_id}")
#     return {"resume_id": resume_id, "message": "Resume ID received"}
