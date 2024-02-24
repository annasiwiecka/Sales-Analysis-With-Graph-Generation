from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm


def logout(request):
    logout(request)
    return redirect('login')

def login(request):
    error_message = None
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=user, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))
                else:
                    return redirect("sales:home")
        else:
            error_message = "something went wrong"

    return render(
        request, "auth/login.html", {"form": form, "error_message": error_message}
    )
