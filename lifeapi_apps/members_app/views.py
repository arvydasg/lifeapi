from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def members_login_user(request):
    # did the user simply come to this page or he actually submitted the form?
    # by checking the request method we can know that
    if request.method == "POST":
        # taking "username" and "password" from the form "name" attribute
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # If a variable contains None, it means that it doesn't point to any valid object or data.
        # not None == username and password exists
        if user is not None:
            login(request, user)
            messages.success(request, ("You Were Logged in!"))
            next_url = request.POST.get('next')  # Get the 'next' parameter from POST data(from members_login.html template)
            if next_url:
                return redirect(next_url)  # Redirect to 'next' URL if it exists
            else:
                return redirect('home')  # Redirect to 'home' URL if 'next' doesn't exist
        else:
            messages.success(request, ("There was an Error logging in, Try Again..."))
            return redirect('members_login_user')

    # if the user simply came to this page without submitting the form
    # display the login template
    else:
        return render(request, 'members/members_login.html', {})

def members_logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return redirect('home')


def members_register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save() # save their filled information
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, ("Registration Successful!"))
            return redirect('home')
    else:
        form = RegisterUserForm()

    return render(request, 'members/members_register.html', {'form': form,})


@login_required
def members_dashboard(request):
    return render(request, 'members/members_dashboard.html')