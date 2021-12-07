from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LogInForm, UserForm, PasswordForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
# from .forms import LogInForm, PasswordForm, PostForm, UserForm, SignUpForm
from .forms import LogInForm, SignUpForm
from .models import User
from .helpers import login_prohibited

@login_prohibited
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        next = request.POST.get('next') or ''
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_member:
                login(request, user)
                redirect_url = next or 'feed'
                return redirect(redirect_url)
            else:
                messages.add_message(request, messages.ERROR, "Your application is still being processed, please wait to be able to log in")
        else:
            messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    else:
        next = request.GET.get('next') or ''
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form, 'next': next})

@login_prohibited
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')

    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('home')

@login_prohibited
def home(request):
    return render(request, 'home.html')

@login_required
def feed(request):
    return render(request, 'feed.html')

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

@login_required
def show_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect('user_list')
    else:
        #return render(request, 'show_user.html', {'user': user})
        current_user = request.user
        if (current_user.is_member):
            return render(request, 'show_user.html', {'current_user': current_user, 'user': user})
        if current_user.is_officer:
            return render(request, 'officer_show_user.html', {'current_user': current_user, 'user': user})
        if current_user.is_owner:
            return render(request, 'owner_show_user.html', {'current_user': current_user, 'user': user})

def profile(request):
    current_rank = ""
    user= request.user
    if user.is_applicant:
        current_rank = "Applicant"
    if user.is_officer:
        current_rank = "Officer"
    if user.is_owner:
        current_rank = "Owner"
    if user.is_member:
        current_rank = "Member"
    return render(request, 'profile.html', {'user':user, 'current_rank':current_rank})

def promote_to_member(request, user_id):
    user = request.user
    current_user = User.objects.get(id=user_id)
    if ((user.is_officer or user.is_owner) and current_user.is_applicant) or user.is_owner:
        current_user.is_applicant = False
        current_user.is_member = True
        current_user.is_officer = False
        current_user.save(update_fields=["is_applicant"])
        current_user.save(update_fields=["is_member"])
        current_user.save(update_fields=["is_officer"])
    return redirect("profile")

def promote_to_officer(request, user_id):
    user = request.user
    current_user = User.objects.get(id=user_id)
    if current_user.is_member:
        current_user.is_member = False
        current_user.is_officer = True
        current_user.save(update_fields=["is_officer"])
        current_user.save(update_fields=["is_member"])
    return redirect("profile")

def transfer_ownership(request, user_id):
    user = request.user
    current_user = User.objects.get(id=user_id)
    if (user.is_owner and current_user.is_officer):
        user.is_owner = False
        current_user.is_owner = True
        user.is_officer = True
        current_user.is_officer = False
        current_user.save(update_fields=["is_officer"])
        current_user.save(update_fields=["is_owner"])
        user.save(update_fields=["is_officer"])
        user.save(update_fields=["is_owner"])
    return redirect("profile")


@login_required
def password(request):
    current_user = request.user
    if request.method == 'POST':
        form = PasswordForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if check_password(password, current_user.password):
                new_password = form.cleaned_data.get('new_password')
                current_user.set_password(new_password)
                current_user.save()
                login(request, current_user)
                messages.add_message(request, messages.SUCCESS, "Password updated!")
                return redirect('feed')
    form = PasswordForm()
    return render(request, 'password.html', {'form': form})


@login_required
def changeprofile(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserForm(instance=current_user, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect('feed')
    else:
        form = UserForm(instance=current_user)
    return render(request, 'changeprofile.html', {'form': form})
