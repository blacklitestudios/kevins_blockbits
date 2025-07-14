from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import AbstractUser, CustomUser, Transaction



class RegisterForm(UserCreationForm):
    #email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'bg-gray-800 text-white rounded-lg px-4 py-2 w-full'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'bg-gray-800 text-white rounded-lg px-4 py-2 w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'bg-gray-800 text-white rounded-lg px-4 py-2 w-full'})
        self.fields['password2'].widget.attrs.update({'class': 'bg-gray-800 text-white rounded-lg px-4 py-2 w-full'})

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()  # This is where password gets hashed
        return user
    
class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'bg-gray-800 text-white rounded-lg px-4 py-2 w-full'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'bg-gray-800 text-white rounded-lg px-4 py-2 w-full'
        })
    
class TransferForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    amount = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'bg-gray-800 text-white rounded-lg px-4 py-2 w-1/2'
        })
        self.fields['amount'].widget.attrs.update({
            'class': 'bg-gray-800 text-white rounded-lg px-4 py-2 w-1/2'
        })
        

    def save(self, commit=True):
        # Case-sensitive exact match
        try:
            user = get_user_model().objects.get(username=self.cleaned_data['username'])
            amount = self.cleaned_data['amount']
            if self.user.balance < amount and not self.user.is_superuser:
                raise forms.ValidationError("Insufficient balance to complete the transfer.")
            if not self.user.is_superuser and self.cleaned_data['amount'] < 1:
                raise forms.ValidationError("Transfer value must be positive.")
            if not self.user.is_superuser and self.cleaned_data['username'] == self.user.username:
                raise forms.ValidationError("You can't send money to yourself.")


            user.balance += amount
            self.user.balance -= amount
            Transaction.objects.create(
                user=self.user,
                amount=-amount
            )
            Transaction.objects.create(
                user=user,
                amount=amount
            )
            if self.user.is_superuser:
                self.user.balance = 0.00
            if commit:
                self.user.save()
                user.save()
            
        except get_user_model().DoesNotExist:
            # Handle user not found
            user = None