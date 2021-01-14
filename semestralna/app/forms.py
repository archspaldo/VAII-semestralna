from django.core import validators
from django import forms
from django.contrib.auth import authenticate, login, get_user_model as User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _



class DiscussionForm(forms.Form):
    title = forms.CharField(label='Názov diskúsie',
                            max_length=255, min_length=3)
    description = forms.CharField(
        widget=forms.Textarea, label='Popis diskusie')


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    """
    class Meta:
        model = User()
        fields = ['username', 'password']
        labels = {
            'username': _('Prihlasovacie meno'),
            'password': _('Heslo'),
        }
        help_texts = {
            'username': None,
        }

    """
    username = forms.CharField(
        label='Prihlásovacie meno',
        max_length=31, min_length=3, strip=True, 
        error_messages={
            'required': 'Toto pole je povinne',
        })
    password = forms.CharField(widget=forms.PasswordInput, label='Heslo')
    
    def clean(self):
        cleaned_data = self.cleaned_data
        if 'username' not in cleaned_data:
            return cleaned_data
        user = User().objects.filter(username=cleaned_data['username']).first() if 'username' in cleaned_data else None
        if user is None or user.check_password(cleaned_data['password']) == False:
            self.add_error('username', forms.ValidationError(_('Neznáme meno'), code ='invalid'))
            self.add_error('password', forms.ValidationError(_('Neznáme heslo'), code='invalid'))
        return cleaned_data
  



        


        

