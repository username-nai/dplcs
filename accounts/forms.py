from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=True, help_text='Required. Unique phone number.')
    email = forms.EmailField(required=True, help_text='Required. Unique email address.')
    name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ('name', 'phone', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['name'] # Using first_name as name for simplicity, or we can use a custom name field. 
        # But since AbstractUser has first_name and last_name, we can just use first_name, or we can add a 'name' field to User.
        # Wait, the prompt asked for "Name". I'll map it to first_name.
        user.username = self.cleaned_data['phone'] # Use phone as username for simplicity, or generate one.
        if commit:
            user.save()
        return user
