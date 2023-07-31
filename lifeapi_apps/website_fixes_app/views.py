from django.shortcuts import render, redirect, get_object_or_404
from .models import WebsiteFix
from .forms import WebsiteFixForm
from django.contrib.auth.decorators import login_required
from .forms import ViewFixesForm


def website_fixes_app_home(request):
    return render(request, 'website_fixes/home.html')


def website_fixes(request):
    fixes = WebsiteFix.objects.all()
    not_fixed_fixes = WebsiteFix.objects.filter(status='Not Fixed')
    total_fixes_count = not_fixed_fixes.count()

    view_form = ViewFixesForm(request.GET or None)  # Bind the form with the submitted data (GET request)

    if view_form.is_valid():
        view_option = view_form.cleaned_data['view_option']
        if view_option == 'user':
            # Filter fixes for the current authenticated user
            if request.user.is_authenticated:
                fixes = WebsiteFix.objects.filter(user=request.user)
        else:
            # Show all fixes
            fixes = WebsiteFix.objects.all()

    context = {
        'fixes': fixes,
        'total_fixes_count': total_fixes_count,
        'view_form': view_form,
    }
    
    return render(request, 'website_fixes/website_fixes.html', context)


@login_required
def add_website_fix(request):
    if request.method == 'POST':
        form = WebsiteFixForm(request.POST)
        if form.is_valid():
            website_fix = form.save(commit=False)  # Don't save the form yet
            website_fix.user = request.user  # Set the 'user' field to the current user
            website_fix.save()  # Save the form with the associated user
            return redirect('website_fixes') # Redirect to the view that displays the fixes
    else:
        form = WebsiteFixForm()

    context = {
        'form': form,
    }
    
    return render(request, 'website_fixes/add_website_fix.html', context)


@login_required
def preview_website_fix(request, fix_id):
    fix = get_object_or_404(WebsiteFix, id=fix_id)
    
    context = {
        'fix': fix,
    }

    return render(request, 'website_fixes/preview_website_fix.html', context)


@login_required
def edit_website_fix(request, fix_id):
    fix = get_object_or_404(WebsiteFix, id=fix_id)

    if request.method == 'POST':
        form = WebsiteFixForm(request.POST, instance=fix)
        if form.is_valid():
            form.save()
            return redirect('website_fixes')
    else:
        form = WebsiteFixForm(instance=fix)

    context = {
        'form': form,
    }

    return render(request, 'website_fixes/edit_website_fix.html', context)


@login_required
def delete_website_fix(request, fix_id):
    fix = get_object_or_404(WebsiteFix, id=fix_id)

    if request.method == 'POST':
        fix.delete()
        return redirect('website_fixes')
    
    context = {
        'fix': fix,
    }

    return render(request, 'website_fixes/delete_website_fix.html', context)