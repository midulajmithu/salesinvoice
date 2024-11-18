from django.contrib.auth import authenticate, login
from .models import CustomUser
from django.contrib.auth.hashers import make_password  # To hash the password
from django.contrib import messages  # To display error messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404


@login_required(login_url="sign_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_list(request):
    users = CustomUser.objects.filter(user_type='normal')
    return render(request, 'user_list.html', {'users': users})

def set_inactive(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = False
    user.save()
    return redirect('user_list')

def delete_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
      #  messages.success(request, "User deleted successfully.")
        return redirect('user_list')  # Redirect back to the user list page

def update_user(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        username = request.POST.get("username")
        name = request.POST.get("name")
        status = request.POST.get("status") == "True"
        password = request.POST.get("password")

        user = get_object_or_404(CustomUser, id=user_id)
        user.username = username
        user.name = name
        user.is_active = status

        # Update password only if a new one is provided
        if password:
            user.password = make_password(password)

        user.save()

        return redirect("user_list")  # Redirect to the user list view
    
def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')

        # Simple validation
        if not username or not password or not name:
            messages.error(request, "All fields are required.")
            return render(request, 'sign_up.html')

        # Check if username is unique
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'sign_up.html')

        # Create a new user with a hashed password
        user = CustomUser(
            username=username,
            name=name,
            user_type='normal'  # Default user type
        )
        user.set_password(password)  # Hash the password using set_password
        user.save()
        
        messages.success(request, "Registration successful!")
        return redirect('sign_in')  # Redirect to login page

    return render(request, 'user/sign_up.html')

def admin_useradd(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')

        # Simple validation
        if not username or not password or not name:
            messages.error(request, "All fields are required.")
            return render(request, 'add_user.html')

        # Check if username is unique
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'add_user.html')

        # Create a new user with a hashed password
        user = CustomUser(
            username=username,
            name=name,
            user_type='normal'  # Default user type
        )
        user.set_password(password)  # Hash the password using set_password
        user.save()
        
        messages.success(request, "Registration successful!")
        return redirect('sign_in')  # Redirect to login page

    return render(request, 'user/add_user.html')

def sign_in(request):

    

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate using the custom backend
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)  # Log the user in
            if user.user_type == 'normal':
                return redirect('home')  # Redirect normal users to home
            elif user.user_type == 'admin':
                return redirect('admin_dashboard')  # Redirect admin users to dashboard
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'user/sign_in.html')

def custom_logout(request):
    
    storage = messages.get_messages(request)
    list(storage)  # Consume messages to clear them

    # Log the user out
    logout(request)

    # Redirect to the login page (or any page after logout)
    response = redirect('sign_in')  # Replace with your actual login URL or view
    
    # Set headers to prevent caching
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response


