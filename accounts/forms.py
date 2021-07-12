from django import forms
from .models import Account,UserProfile

class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder':'Enter Password'
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder':'Confirm Password'
    }))
    # first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'pattern':'[A-Za-z ]+','placeholder':'Enter First Name', 'title':'Enter Characters Only '}))
    class Meta:
        model=Account
        fields=['first_name','last_name','email','phone_number','password']

    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter Last Name'
        self.fields['email'].widget.attrs['placeholder']='Enter Email'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter Phone Number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] ='form-control'

    def clean(self):
               cleaned_data = super(RegistrationForm, self).clean()
               password = cleaned_data.get('password')
               confirm_password = cleaned_data.get('confirm_password')
               fname=cleaned_data.get('first_name')
               lname=cleaned_data.get('last_name')
               if password != confirm_password:
                   raise forms.ValidationError('Password does not match')
               else:
                   if len(password) <8:
                       raise forms.ValidationError('The Pasword is to short')
               if len(fname)<4 and  (lname) < 4:
                   raise forms.ValidationError('Name must be more then 4 character')



class UserForm(forms.ModelForm):
    class Meta:
        model =Account
        fields = ['first_name','last_name','phone_number']
    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] ='form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture =forms.ImageField(required=False,error_messages ={'invalid':("Image file only")},widget=forms.FileInput)
    class Meta:
        model=UserProfile
        fields = ['address_line_1','address_line_2','city','state','profile_picture']
    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] ='form-control'
