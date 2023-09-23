from django import forms
from .models import Meetup,myUser,Participant,Speaker,Testimonial
from django.contrib.auth.forms import UserCreationForm
# from django.forms import TextInput,PasswordInput,EmailInput, FileInput
from django.core.validators import EmailValidator

class MyUserRegistrationForm(UserCreationForm):
    class Meta:
        model = myUser
        fields = [ 'name', 'username', 'email', 'password1','password2', 'image',]
        widgets={
            'name': forms.TextInput(attrs={'placeholder': 'Enter name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
        }


class UseMeetupForm(forms.ModelForm):
    class Meta:
        model = Meetup
        fields = [ 'title', 'from_date', 'to_date',
                   'meetup_endtime', 'description', 'image', 'organizer_email', 
                   'location_name', 'location_address', 'activate',
                ]
        widgets={
           'title':forms.TextInput(attrs={'placeholder':'Enter meetup title'}),
           'from_date':forms.DateInput(attrs={'placeholder':'yyyy-mm-dd'}),
           'to_date':forms.DateInput(attrs={'placeholder':'yyyy-mm-dd'}),
           'meetup_endtime':forms.TimeInput(attrs={'placeholder':'18:30:00'}),
           'description':forms.Textarea(attrs={'placeholder':'Enter meetup description'}),
           'organizer_email':forms.EmailInput(attrs={'placeholder':'Enter email'}),
           'location_name':forms.TextInput(attrs={'placeholder':'Meetup location'}),
           'location_address':forms.Textarea(attrs={'placeholder':'Meetup location address'}),
        }


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'phone']
       
class SpeakerForm(forms.ModelForm):
    class Meta:
        model = Speaker
        fields = ['name', 'email','proffession', 'phone', 'bio', 'image']
        labels ={
            'name': 'FullName',
            'email': 'Email Address',
            'phone': 'Phone Number',
        }
        widgets={
            'name':forms.TextInput(attrs={'placeholder':'Enter your name'}),
            'email':forms.EmailInput(attrs={'placeholder':'Enter your email'}),
            'proffession':forms.TextInput(attrs={'placeholder':'Enter your proffession'}),
            'phone':forms.NumberInput(attrs={'placeholder':'Enter your Phone number'}),
            'bio':forms.Textarea(attrs={'placeholder':'here...'}),
        }
        
class TestimonialForm(forms.ModelForm):
    class Meta:
        model= Testimonial
        fields= ['name', 'profession', 'comment', 'image']
        
        
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Your name'}))
    email = forms.EmailField(validators=[EmailValidator()], widget=forms.EmailInput(attrs={'placeholder':'Your email'}))
    subject=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Subject...'}))
    message=forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Message...'}))
    