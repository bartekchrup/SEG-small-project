from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LogInForm, UserForm, PasswordForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings
# from .forms import LogInForm, PasswordForm, PostForm, UserForm, SignUpForm
from .forms import LogInForm, SignUpForm, ClubForm
from .models import User, Club
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
            if user is not None:
                login(request, user)
                redirect_url = next or settings.REDIRECT_URL_WHEN_LOGGED_IN
                return redirect(redirect_url)
            else:
                messages.add_message(request, messages.ERROR, "You have entered the wrong username or password")
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
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)

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
def user_list(request):
    try:
        selected_club = request.user.preferredClub
        users_in_club = selected_club.members.all()
    except ObjectDoesNotExist:
        return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    else:
        user_clubs = request.user.member_at.all()
        return render(request, 'user_list.html', {'users': users_in_club, 'user_clubs': user_clubs})

@login_required
def show_user(request, user_id):
    try:
        user_to_show = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect('user_list')
    else:
        user_clubs = request.user.member_at.all()
        current_user = request.user
        current_club = current_user.preferredClub
        if (current_club.is_owner(current_user)):
            return render(request, 'owner_show_user.html', {'current_user': current_user, 'user': user_to_show, 'user_clubs': user_clubs})
        elif (current_club.is_officer(current_user)):
            return render(request, 'officer_show_user.html', {'current_user': current_user, 'user': user_to_show, 'user_clubs': user_clubs})
        elif (current_club.is_member(current_user)):
            return render(request, 'show_user.html', {'current_user': current_user, 'user': user_to_show, 'user_clubs': user_clubs})

@login_required
def profile(request):
    current_rank = ""
    user = request.user
    user_club_memberships = user.member_at.all()
    selected_club = user.preferredClub

    if (selected_club == None):
        if (not user_club_memberships):
            current_rank = "Applicant"
        else:
            messages.add_message(request, messages.ERROR, "Please select a club from 'Your Clubs' to view your profile")
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    else:
        if (selected_club.is_owner(user)):
            current_rank = "Owner"
        elif (selected_club.is_officer(user)):
                current_rank = "Officer"
        elif (selected_club.is_member(user)):
            current_rank = "Member"

    return render(request, 'profile.html', {'user':user, 'current_rank':current_rank, 'user_clubs': user_club_memberships})

@login_required
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

@login_required
def promote_to_officer(request, user_id):
    user = request.user
    current_user = User.objects.get(id=user_id)
    if current_user.is_member:
        current_user.is_member = False
        current_user.is_officer = True
        current_user.save(update_fields=["is_officer"])
        current_user.save(update_fields=["is_member"])
    return redirect("profile")

@login_required
def switch_selected_club(request, club_id):
    user = User.objects.get(id=request.user.id)
    club_to_switch = Club.objects.get(id = club_id)
    user_clubs = request.user.member_at.all()
    if club_to_switch in user_clubs:
        user.preferredClub = club_to_switch
        user.save()
    return redirect('user_list')

@login_required
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
                return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    form = PasswordForm()
    user_clubs = request.user.member_at.all()
    return render(request, 'password.html', {'form': form, 'user_clubs': user_clubs})


@login_required
def changeprofile(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserForm(instance=current_user, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    else:
        form = UserForm(instance=current_user)
    user_clubs = request.user.member_at.all()
    return render(request, 'changeprofile.html', {'form': form, 'user_clubs': user_clubs})

@login_required
def clubs_list(request):
    clubs = Club.objects.all()
    user_clubs = request.user.member_at.all()
    return render(request, 'clubs_list.html', {'clubs': clubs, 'user_clubs': user_clubs})

@login_required
def create_club(request):
    if request.method=='POST':
        form = ClubForm(request.POST)
        user = request.user
        if form.is_valid():
            club_name = form.cleaned_data.get('club_name')
            club_location = form.cleaned_data.get('club_location')
            club_description = form.cleaned_data.get('club_description')
            club = Club.objects.create(club_owner = user, club_name = club_name, club_location = club_location, club_description = club_description)
            messages.add_message(request, messages.SUCCESS, "New Club has been successfully created!")
            return redirect('show_club', club.id)
    else:
        form = ClubForm()
    user_clubs = request.user.member_at.all()
    return render(request, 'create_club.html', {'form': form, 'user_clubs': user_clubs})

@login_required
def show_club(request, club_id):
    try:
        club = Club.objects.get(id=club_id)
    except ObjectDoesNotExist:
        return redirect('home')
    else:
        user_clubs = request.user.member_at.all()
        return render(request, 'show_club.html',{'club': club, 'user_clubs': user_clubs})
