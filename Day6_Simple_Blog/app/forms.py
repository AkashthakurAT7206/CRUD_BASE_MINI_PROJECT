from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Blog,Category,Profile,Comment,Tag


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True,max_length=50)
    last_name = forms.CharField(required=True,max_length=50)
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email','password1','password2')
    

    
    def save(self,commit=True):
        user = super().save(commit=False)
        user.email =self.cleaned_data['email']
        user.first_name =self.cleaned_data['first_name']
        user.last_name =self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
    
    
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','location','birth_date','avatar','website']
        
        widgets = {
            # bio : forms.Textarea(attrs={'azad':'azad'})
            'bio' : forms.Textarea(attrs={'rows':4}),
            'birth_date' : forms.DateInput(attrs={'type':'date','idk':'azad'}),
            'location' : forms.TextInput(attrs={'placeholder':'enter your location'}),
            'avatar': forms.ClearableFileInput(attrs={'accept': 'image/*'}),  
            'website' : forms.URLInput(attrs={'placeholder':'enter your web site'})
        }
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'slug', 'content', 'featured_image', 'category', 'tags', 'is_published']
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name',]
             
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
      model = User
      fields = ['username','email','first_name','last_name']