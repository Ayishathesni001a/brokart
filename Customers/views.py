# In Customers/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Customer
from django.contrib import messages

def sign_out(request):
    logout(request)
    return redirect('home')

def show_account(request):
    context = {}
    
    if request.method == 'POST':
        if 'register' in request.POST:
            context['register'] = True

            # Get the form data
            username = request.POST.get('Username')
            password = request.POST.get('Password')
            email = request.POST.get('Email')
            address = request.POST.get('Address')
            phone = request.POST.get('Phone')

            try:
                # Create user account
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                )

                # Create customer account
                customer = Customer.objects.create(
                    user=user,  # Use the user instance created above
                    phone=phone,
                    address=address
                )
                customer.save()

                messages.success(request, "User registered successfully")
                login(request, user)  # Log the user in after registration
                return redirect('account')  # Redirect to the account page or profile

            except Exception as e:
                messages.error(request, "Username already exists or invalid inputs")

        elif 'login' in request.POST:
            context['register'] = False

            username = request.POST.get('Username')
            password = request.POST.get('Password')
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                # Check if the user has a customer profile
                
                return redirect('home')  # Redirect to profile creation view if not

            else:
                messages.error(request, 'Invalid username or password')

    return render(request, 'account.html', context)

