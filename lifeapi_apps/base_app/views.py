from django.shortcuts import render, redirect, get_object_or_404
from .models import WebsiteFix
from .forms import WebsiteFixForm
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


def website_fixes(request):
    fixes = WebsiteFix.objects.all()
    not_fixed_fixes = WebsiteFix.objects.filter(status='Not Fixed')
    total_fixes_count = not_fixed_fixes.count()

    context = {
        'fixes': fixes,
        'total_fixes_count': total_fixes_count,
    }
    
    return render(request, 'website_fixes/website_fixes.html', context)


@login_required
def add_website_fix(request):
    if request.method == 'POST':
        form = WebsiteFixForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('website_fixes')
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