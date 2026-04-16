from __future__ import annotations

from typing import TYPE_CHECKING
import logging
from rest_framework import viewsets
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

logger = logging.getLogger("taskproject.todos")

if TYPE_CHECKING:
    from django.contrib.auth.base_user import AbstractBaseUser
    from django.contrib.auth.models import AnonymousUser

    class AuthHttpRequest(HttpRequest):
        """HttpRequest after AuthenticationMiddleware (has .user)."""

        user: AbstractBaseUser | AnonymousUser

else:
    AuthHttpRequest = HttpRequest


def signup_view(request: AuthHttpRequest) -> HttpResponse:
    """Signup view for the todo app.

    Args:
        request (AuthHttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
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
            # WARNING: Log validation failures such as User error/Unexpected conditons
            logger.warning(
                "Signup validation failed for user: %s", 
                username, 
                extra={"validation_errors": errors}
            )
            return render(
                request,
                "todos/signup.html",
                {"errors": errors, "username": username},
            )
        
        try:
            #STATE CHANGE: Logging a new database record creation
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            logger.info(
                "New user created: %s", 
                username, 
                extra={"user_id": user.id}
            )
            return redirect("task_list")
        except Exception as e:
            # ERROR: Unexpected system failure during user creation to DB
            logger.error(
                "Critical error occurred while creating user: %s", 
                username, 
                exc_info=True
            )
            return render(
                request, 
                "todos/signup.html", 
                {"errors": ["An error occurred while creating the user."], 
                 "username": username}
            )
    return render(
        request, 
        "todos/signup.html", 
        {"errors": [], "username": ""}
        )


def login_view(request: AuthHttpRequest) -> HttpResponse:
    """Login view for the todo app.

    Args:
        request (AuthHttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.user.is_authenticated:
        return redirect("task_list")
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #INFO: Log key user action
            logger.info(
                "User logged in: %s", 
                username, 
                extra={"user_id": user.id}
            )
            return redirect("task_list")
        else:
            #WARNING: Log failed login attempt, potential security concern
            logger.warning(
                "Failed login attempt for username: %s", 
                username
            )
        messages.error(request, "Invalid username or password.")
    return render(request, "todos/login.html")
