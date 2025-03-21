from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Job, Application
from .forms import RegisterForm, ApplicationForm

def home(request):
    """Default Home Page"""
    if request.user.is_authenticated:
        return redirect("job_list")  
    return redirect("register")  

def register(request):
    """User Registration"""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("job_list")
    else:
        form = RegisterForm()
    return render(request, "jobs/register.html", {"form": form})

@login_required
def job_list(request):
    """List of Available Jobs"""
    jobs = Job.objects.all()
    return render(request, "jobs/job_list.html", {"jobs": jobs})

@login_required
def job_detail(request, job_id):
    """Job Details with Apply Option"""
    job = get_object_or_404(Job, id=job_id)
    already_applied = Application.objects.filter(user=request.user, job=job).exists()
    return render(request, "jobs/job_detail.html", {"job": job, "already_applied": already_applied})

@login_required
def apply_for_job(request, job_id):
    """Apply for a Job (Prevent Duplicate Applications)"""
    job = get_object_or_404(Job, id=job_id)

    if Application.objects.filter(user=request.user, job=job).exists():
        return redirect("job_list")  

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.job = job
            application.save()
            return redirect("job_list")
    else:
        form = ApplicationForm()

    return render(request, "jobs/apply.html", {"form": form, "job": job})

@login_required
def user_applications(request):
    applications = Application.objects.filter(user=request.user)
    return render(request, "jobs/user_applications.html", {"applications": applications})