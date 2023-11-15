from multiprocessing import context
from django.shortcuts import redirect, render, reverse
from .forms import CreateUserForm, LoginForm, ThoughtPostForm, ThoughtUpdateForm, UpdateUserForm, UpdateProfileForm
from .models import Thought, Profile
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings



def home(request):
    """ This is the home paoge view """
    return render(request, 'index.html')


def register(request):
    """ This is the register page view """

    form = CreateUserForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():
            current_user = form.save(commit=False)
            form.save()
            send_mail('Welcome to DailyThought!', 'Well done on creating your account', settings.DEFAULT_FROM_EMAIL, [current_user.email])
            # Create a blank object for a single instance with FK attached
            profile = Profile.objects.create(user=current_user)

            messages.success(request, 'Your account was created successfully!')

            return redirect('user-login')
    else:
        form = CreateUserForm()
    context = {
        'form':form,
    }
    return render(request, 'register.html', context)


def user_login(request):
    """ This is the login page view """

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Login success!')
                return redirect(reverse('dashboard'))
        else:
            form = LoginForm()
    context = {
        'form':form,
    }
    return render(request, 'user-login.html', context)


def user_logout(request):
    """ This is the logout page view """

    auth.logout(request)
    messages.success(request, 'Logout success!')
    return redirect('user-login')


@login_required(login_url='user-login')
def dashboard(request):
    """ This view render's the dashboard """

    profile_pic = Profile.objects.get(user=request.user)

    context = {
        'user_profile_pic': profile_pic,
    }

    return render(request, 'profile/dashboard.html', context)


@login_required(login_url='user-login')
def post_thought(request):
    """ This view gives users the ability to post their thoughts"""

    form = ThoughtPostForm()

    if request.method == 'POST':
        form = ThoughtPostForm(request.POST)

        if form.is_valid():

            thought = form.save(commit=False)
            thought.user = request.user
            thought.save()

            messages.success(request, 'You have posted a new thought!')

            return redirect(reverse('my-thoughts'))
    
    context = {
        'form': form,
    }

    return render(request, 'profile/post-thought.html', context)


@login_required(login_url='user-login')
def my_thoughts(request):
    """ This view gives users the ability to view their thoughts"""

    current_user = request.user.id

    thought = Thought.objects.all().filter(user=current_user)

    context = {
        'thoughts': thought,
    }

    return render(request, 'profile/my-thoughts.html', context)


@login_required(login_url='user-login')
def update_thought(request, pk):
    """ This view gives users the ability to update their thoughts"""

    thought = Thought.objects.get(id=pk)

    form = ThoughtUpdateForm(instance=thought)

    if request.method == 'POST':

        form = ThoughtUpdateForm(request.POST, instance=thought)

        if form.is_valid():

            form.save()

            messages.success(request, 'You have updated your thought!')

            return redirect('my-thoughts')

    context = {
        'form': form,
    }

    return render(request, 'profile/update-thought.html', context)


@login_required(login_url='user-login')
def delete_thought(request, pk):
    """ This view gives users the ability to delete their thoughts"""

    thought = Thought.objects.get(id=pk)

    if request.method == 'POST':
            
            thought.delete()

            messages.success(request, 'You have deleted a thought!')

            return redirect('my-thoughts')

    return render(request, 'profile/delete-thought.html',)


@login_required(login_url='user-login')
def profile_management(request):
    """ This view gives users the ability to manage their profile"""

    form = UpdateUserForm(instance=request.user)

    profile = Profile.objects.get(user=request.user)

    # Profile form for profile picture
    profile_form_update = UpdateProfileForm(instance=profile)

    if request.method == 'POST':

        form = UpdateUserForm(request.POST, instance=request.user)

        profile_form_update = UpdateProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():

            form.save()

            messages.success(request, 'Your username/email was updated successfully!')

        elif profile_form_update.is_valid():

            profile_form_update.save()

            messages.success(request, 'Your profile picture was updated successfully!')

        return redirect('dashboard')

    context = {
        'form': form,
        'profile_form_update': profile_form_update,
    }

    return render(request, 'profile/profile-management.html', context)


@login_required(login_url='user-login')
def delete_account(request):
    """ This view gives users the ability to delete their account"""

    if request.method == 'POST':

        delete_user = User.objects.get(username=request.user)

        delete_user.delete()

        messages.success(request, 'Your account was deleted successfully!')

        return redirect('user-login')
    
    return render(request, 'profile/delete-account.html')