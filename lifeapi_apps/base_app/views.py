from django.shortcuts import render, redirect, get_object_or_404
from .models import WebsiteFix
from .forms import WebsiteFixForm


def home(request):
    return render(request, 'home.html')


def website_fixes(request):
    if request.method == 'POST':
        form = WebsiteFixForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('website_fixes')
    else:
        form = WebsiteFixForm()

    fixes = WebsiteFix.objects.all().order_by('-date_created')

    context = {
        'form': form,
        'fixes': fixes,
    }
    
    return render(request, 'website_fixes.html', context)


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

    return render(request, 'edit_website_fix.html', context)


def delete_website_fix(request, fix_id):
    fix = get_object_or_404(WebsiteFix, id=fix_id)

    if request.method == 'POST':
        fix.delete()
        return redirect('website_fixes')
    
    context = {
        'fix': fix,
    }

    return render(request, 'delete_website_fix.html', context)