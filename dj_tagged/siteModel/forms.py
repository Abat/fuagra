from django import forms
from siteModel.models import User
from siteModel.models import UserProfile
import string

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	email_address = forms.CharField(widget=forms.EmailInput())
	MIN_USERNAME_LENGTH = 4
	MIN_PASSWORD_LENGTH = 8

	class Meta:
		model = User
		fields = ('username', 'password')

	def is_valid(self):
 
        # run the parent validation first
        valid = super(UserForm, self).is_valid()
 
        # we're done now if not valid
        if not valid:
            return valid

        if (!self._validate_user_name(user_form.cleaned_data.get('username'))):
        	self._errors['username'] = 'BadUserName'
        	return False
        if (!self._validate_password(user_form.cleaned_data.get('password'))):
        	self._errors['password'] = 'BadPassword'
 			return False
        # all good
        return True

    #Actually I dunno, think this is directed to non-english.
    def _validate_user_name(self, username):
    	if (not username or username.len() < self.MIN_USERNAME_LENGTH):
    		return False
    	ALPHA = string.ascii_letters
		if not username.startswith(tuple(ALPHA)):
		   return False 
		if not username.isalnum():
		   return False 
    	return True

    def _validate_password(password):
    	if (not password or password.len() < self.MIN_PASSWORD_LENGTH):
    		return False
    	return True

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('avatar',)