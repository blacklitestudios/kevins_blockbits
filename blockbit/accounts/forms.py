from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import AbstractUser, CustomUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()  # This is where password gets hashed
        return user
    
class TransferForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    amount = forms.IntegerField(min_value=1, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.pop('user', None)

    def save(self, commit=True):
        # Case-sensitive exact match
        try:
            user = get_user_model().objects.get(username='target_username')
            user.balance += self.cleaned_data['amount']
            self.user.balance -= self.cleaned_data['amount']
            if commit:
                self.user.save()
                user.save()
            
        except get_user_model().DoesNotExist:
            # Handle user not found
            user = None