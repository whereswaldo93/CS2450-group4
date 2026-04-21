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

    # Initial entry
    logger.debug(
        "Signup page accessed successfully with authenticated status %s",
        request.user.is_authenticated
    )

    if request.user.is_authenticated:
        return redirect("task_list")
    
    if request.method == "POST":
        # Log payload without sensitive info
        logger.debug(
            "Signup attempt for username: %s", request.POST.get("username")
        )

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
            # Potential common user error
            logger.warning("Signup attempt with existing username %s", username)
            errors.append("Username is already taken.")

        if errors:
            # Log validation failures such as User error/Unexpected conditons
            logger.warning(
                "Signup validation failed for user %s with error: %s", 
                username, 
                errors
            )
            return render(
                request,
                "todos/signup.html",
                {"errors": errors, "username": username},
            )
        
        try:
            # Logging a new database record creation
            user = User.objects.create_user(username=username, password=password1)

            # New user successfully created
            logger.info("New user %s account created with ID: %s",
                username,
                request.user.id
            )

            login(request, user)

            # Starting session after login
            logger.info(
                "User %s logged in after sign up", 
                username
            )
            return redirect("task_list")
        
        except Exception as e:
            # Unexpected system failure during user creation to DB
            logger.error(
                "Critical error occurred while creating user %s: %s", 
                username,
                str(e),
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

        # Log the intenttn of creating username and password, not the pasword itself
        logger.debug("Login attempt started for user %s", username)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Log key user action
            logger.info(
                "User %s with ID %s successfully logged in", 
                username, 
                request.user.id
            )
            return redirect("task_list")
        else:
            # Log failed login attempt, potential security concern
            logger.warning(
                "Failed login attempt for user %s", 
                username
            )
        messages.error(request, "Invalid username or password.")
    return render(request, "todos/login.html")
