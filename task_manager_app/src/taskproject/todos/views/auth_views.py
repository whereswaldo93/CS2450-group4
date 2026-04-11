from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def signup_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("task_list")
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password1 = request.POST.get("password1") or ""
        password2 = request.POST.get("password2") or ""
        errors: list[str] = []
        if not username:
            errors.append("Username is required.")
        if not password1:
            errors.append("Password is required.")
        elif password1 != password2:
            errors.append("Passwords do not match.")
        else:
            try:
                validate_password(password1, User(username=username))
            except ValidationError as e:
                errors.extend(e.messages)
        if User.objects.filter(username=username).exists():
            errors.append("That username is already taken.")
        if errors:
            return render(
                request,
                "todos/signup.html",
                {"errors": errors, "username": username},
            )
        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        return redirect("task_list")
    return render(request, "todos/signup.html", {"errors": [], "username": ""})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("task_list")
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("task_list")
        messages.error(request, "Invalid username or password.")
    return render(request, "todos/login.html")
