from django import forms
from django.forms import fields, widgets
from.models import Friend, Message


class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['name', 'mail', 'gender', 'age', 'birthday']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control'}),
        }

class FindForm(forms.Form):
    find = forms.CharField(label='Find', required=False, \
        widget=forms.TextInput(attrs={'class':'form-control'}))

class CheckForm(forms.Form):
    str = forms.CharField(label='String', \
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    def clean(self):
        cleaned_data = super().clean()
        str = cleaned_data['str']
        if (str.lower().startswith('no')):
            raise forms.ValidationError('You input "NO"!') # エラーを発生させる

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'content', 'friend']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'content': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows':2}),
            'friend': forms.Select(attrs={'class':'form-control form-control-sm'}),
        }



    # date = forms.DateField(label='Date', input_formats=['%d'], \
    #     widget=forms.DateInput(attrs={'class': 'form-control'}))
    # time = forms.TimeField(label='Time', \
    #     widget=forms.TimeInput(attrs={'class': 'form-control'}))
    # datetime = forms.DateTimeField(label='DateTime', \
    #     widget=forms.DateTimeInput(attrs={'class': 'form-control'}))

    # required = forms.IntegerField(label='Required', \
    #     widget=forms.NumberInput(attrs={'class': 'forms-control'}))
    # min = forms.IntegerField(label='Min', min_value=100, \
    #     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    # max = forms.IntegerField(label='Max', max_value=1000, \
    #     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    # empty = forms.CharField(label='Empty', empty_value=True, \
    #     widget=forms.TextInput(attrs={'class':'form-control'}))



# class HelloForm(forms.Form):
#     name = forms.CharField(label='Name', \
#         widget=forms.TextInput(attrs={'class': 'form-control'}))
#     mail = forms.EmailField(label='Email', \
#         widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     gender = forms.BooleanField(label='Gender', required=False, \
#         widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
#     age = forms.IntegerField(label='Age', \
#         widget=forms.NumberInput(attrs={'class': 'form-control'}))
#     birthday = forms.DateField(label='Birth', \
#         widget=forms.DateInput(attrs={'class': 'form-control'}))

