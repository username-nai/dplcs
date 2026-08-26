from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import User

def home(request):
    if request.user.is_authenticated:
        if request.user.is_admin_role:
            return redirect('admin_dashboard')
        return redirect('user_dashboard')
    return render(request, 'accounts/home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Check if email is unique (User model doesn't enforce it by default in all db engines depending on settings)
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already in use.")
                return render(request, 'accounts/signup.html', {'form': form})
            
            user = form.save()
            messages.success(request, f"Registration successful! Your Member ID is {user.member_id}.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid Member ID or password.")
        return super().form_invalid(form)

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')
