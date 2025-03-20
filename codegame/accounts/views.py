from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from accounts.models import PlayerProfile


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        # Get the email from the POST data (if provided in your template)
        email = request.POST.get('email', '')

        # Simple email validation
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address.")
            # Re‐render the form with the entered data
            return render(request, 'accounts/signup.html', {'form': form})

        if form.is_valid():
            # Create the user object but don't save to DB yet
            user = form.save(commit=False)
            # Assign the validated email
            user.email = email
            # Now save the user to DB (password is already handled by the form)
            user.save()

            messages.success(request, "Registration successful. Please log in.")
            # Redirect to the login page after successful registration
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Credentials correct, now check if user has already played
            profile = PlayerProfile.objects.get(user=user)
            if profile.has_played:
                # Show "Already Played :)" at the top (success block)
                messages.success(request, "Already Played :)")
                return redirect('login')
            else:
                # User can still play, log them in and go to the game
                auth_login(request, user)
                return redirect('game')
        else:
            # Either username doesn't exist or password is wrong
            # Check if the username exists at all
            if User.objects.filter(username=username).exists():
                messages.error(request, "Incorrect password.")
            else:
                messages.error(request, "No account found with that username.")
            return redirect('login')

    # If GET, just show the login form
    return render(request, 'accounts/login.html')

def logout_view(request):
    auth_logout(request)
    # Redirect to home after logout
    return redirect('home')
