from django import forms
from siteModel.models import User
from siteModel.models import UserProfile
from django.core.exceptions import ValidationError
import string

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	email_address = forms.CharField(widget=forms.EmailInput(), required=False)
	MIN_USERNAME_LENGTH = 4
	MIN_PASSWORD_LENGTH = 8

	class Meta:
		model = User
		fields = ('username', 'password')

	def clean(self):
 		data = self.cleaned_data
 		errorMsg = "";

 		username = data.get('username')
 		if (not self._validate_user_name(username)):
 			errorMsg = errorMsg + ('Your username is invalid.')

 		if (not self._validate_password(data.get('password'))):
 			errorMsg = errorMsg + (' Your password is invalid.')

 		if (self._username_exists(username)):
 			errorMsg = errorMsg + (' Your username "%s" is taken.' % username)

 		if (errorMsg):
 			raise ValidationError(errorMsg)

 		return data

    #Actually I dunno, think this is directed to non-english.
	def _validate_user_name(self, username):
		if (not username or len(username) < self.MIN_USERNAME_LENGTH):
			return False
		ALPHA = string.ascii_letters
		if not username.startswith(tuple(ALPHA)):
		   return False 
		if not username.isalnum():
		   return False 
		return True

	def _validate_password(self, password):
		if (not password or len(password) < self.MIN_PASSWORD_LENGTH):
			return False
		return True

	def _username_exists(self, username):
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			return False
		return True  

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('avatar',)

