from django import forms


class DiscussionForm(forms.Form):
    title = forms.CharField(label='Názov diskusie', max_length=255)
    description = forms.CharField(
        widget=forms.Textarea, label='Popis diskusie')
