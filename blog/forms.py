from django import forms
from .models import Post, Profile, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Zdjęcie profilowe")
    profile_bio  = forms.CharField(label = 'Opis',widget=forms.Textarea(attrs={'class': "form-control", 'placeholder': 'Opis'}))

    class Meta:
        model = Profile
        fields = ('profile_image','profile_bio' )



class PostForm(forms.ModelForm):
    """
    Form for creating and updating Post instances.
    """
    body = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Napisz swój wpis!',
                'class': 'form-control',
            }
        ),
        label='',
    )

    class Meta:
        model = Post
        exclude = ['user',]


    def clean_body(self):
        body = self.cleaned_data['body']
        if len(body) < 10:
            raise forms.ValidationError("Post jest za krótki.")
        return body


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Adres e-mail'}))
    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Imie'}))
    last_name = forms.CharField(label='', max_length=100,widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Nazwisko'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nick'
        self.fields['username'].label = ''
        self.fields['username'].help_text = ''

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Hasło'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Powtórz hasło'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ''



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dodaj komentarz...'}),
        }



