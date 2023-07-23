from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
            return redirect('home')
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