from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile, WorkerProfile
from .forms import RegisterForm, LoginForm

def home(request):
    return render(request, 'home.html')

def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            is_female = form.cleaned_data['is_female']
            nid = form.cleaned_data['nid']
            nid_image = form.cleaned_data.get('nid_image')
            profile_image = form.cleaned_data.get('profile_image')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            UserProfile.objects.create(
                user=user,
                role=role,
                phone=phone,
                address=address,
                is_female=is_female,
                nid=nid,
                nid_image=nid_image,
                profile_image=profile_image,
            )
            if role == 'worker':
                experience = form.cleaned_data.get('experience') or 0
                pricing = form.cleaned_data.get('pricing') or 0
                WorkerProfile.objects.create(
                    user=user,
                    experience=experience,
                    pricing=pricing,
                )
            login(request, user)
            return redirect('home')
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        profile.phone = request.POST.get('phone', profile.phone)
        profile.address = request.POST.get('address', profile.address)
        if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES['profile_image']
        profile.save()
        return redirect('profile')
    return render(request, 'accounts/edit_profile.html', {'profile': profile})

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')
    return render(request, 'accounts/delete_account.html')