from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Skill

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','username','email','password1','password2']
        labels ={
            'first_name':'Name'
        }
    def __init__(self,*args,**kwargs):
        super(CustomUserCreationForm,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','email','username','location','bio','short_bio','profile_image',
                  'social_gitHub','social_Linkedin',
                  'social_twitter','social_Website']

    def __init__(self,*args,**kwargs):
        super(ProfileEditForm,self).__init__(*args,**kwargs)

        for name,filed in self.fields.items():
            filed.widget.attrs.update({'class':'input'})

class SkillForm(ModelForm):
    class Meta:
        model= Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self,*args,**kwargs):
        super(SkillForm,self).__init__(*args,**kwargs)

        for name,filed in self.fields.items():
            filed.widget.attrs.update({'class':'input'})

