from django import forms
from django.contrib.auth import get_user_model as User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Discussion, Comment



class DiscussionForm(forms.Form):
    title = forms.CharField(label='Názov diskúsie',
                            max_length=255, min_length=3)
    description = forms.CharField(
        widget=forms.Textarea, label='Popis diskusie')


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

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
  
class ReplyForm(forms.Form):
    message = forms.CharField()
    topic = forms.IntegerField()
    parent_id = forms.IntegerField(required=False)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        status = False
        if 'topic' not in cleaned_data:
            self.add_error('topic', forms.ValidationError(_('ID diskusie nesmie byť prázdne'), code ='required'))
            status = True
        if 'message' not in cleaned_data or cleaned_data['message'].strip() == '':
            self.add_error('message', forms.ValidationError(_('Správa nesmie byť prázdna'), code ='required'))
            status = True
        if status:
            return cleaned_data
        comment = Comment.objects.filter(id = cleaned_data['parent_id']).first() if 'parent_id' in cleaned_data else None
        topic = Discussion.objects.filter(id = cleaned_data['topic']).first()
        if comment is not None and comment.discussion_id != topic:
            self.add_error(None, forms.ValidationError(_('Daná otázka nepatrí do diskusie'), code ='invalid'))
        return cleaned_data




        

