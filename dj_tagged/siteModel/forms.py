from django import forms
from siteModel.models import User
from siteModel.models import UserProfile

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	email_address = forms.CharField(widget=forms.EmailInput())

	class Meta:
		model = User
		fields = ('username', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('avatar',)