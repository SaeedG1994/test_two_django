from django .forms import ModelForm
from .models import Project, Review
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','featured_image','tags']

        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }
    def __init__(self,*args,**kwargs):
        super(ProjectForm,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

        # self.fields['title'].widget.attrs.update(
        #     {'class':'input'}
        # )


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']
        labels = {
            'value':'Place your vote',
            'body':'Add a Comment with your vote'
        }

    def __init__(self,*args,**kwargs):
        super(ReviewForm,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
