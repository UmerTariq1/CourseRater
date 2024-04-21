# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

# class CustomUserCreationForm(UserCreationForm):
#     full_name = forms.CharField(max_length=100, required=True, help_text='Enter your full name')

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ("username", "password1", "full_name")  # 'password2' is deliberately omitted

#     def __init__(self, *args, **kwargs):
#         super(CustomUserCreationForm, self).__init__(*args, **kwargs)
#         del self.fields['password2']  # Ensure 'password2' is removed

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         first_name, last_name = (self.cleaned_data['full_name'].split(' ', 1) + [''])[:2]
#         user.first_name = first_name
#         user.last_name = last_name
#         if commit:
#             user.save()
#         return user

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Import your custom user model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "password1", "full_name")  # 'password2' is deliberately omitted

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        del self.fields['password2']  # Ensure 'password2' is removed

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # Assuming you're handling full_name in the CustomUser model
        if commit:
            user.save()
        return user
