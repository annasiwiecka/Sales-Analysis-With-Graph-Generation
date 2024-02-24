from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import ProfileForm

# Create your views here.

@login_required
def my_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your profile has been updated")
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'profiles/main.html', {
        'profile': profile,
        'form': form,
    })