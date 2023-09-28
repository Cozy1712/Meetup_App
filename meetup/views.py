from typing import Any
from django import http
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Meetup,Speaker,Testimonial
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from .forms import UseMeetupForm, MyUserRegistrationForm, ParticipantForm, SpeakerForm, TestimonialForm, ContactForm, ProfileUpdateForm
from django.urls import reverse_lazy
from string import punctuation
from django.db.models import Q
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail, BadHeaderError



# Create your views here.

# Login using FBV
def Login(request):
    if request.user.is_authenticated:
        return redirect('meetup-index')
    
    if request.method == "POST":                    
        email = request.POST.get('email')
        password = request.POST.get('password')
        email.lower()
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'You are now logged in as {email}.')
            return redirect('meetup-index')
        else:
            messages.error(request, 'Invalid Email or Password')
    return render(request, 'meetup/login.html')
  
# Register
def Register(request):
    
    form = MyUserRegistrationForm()
    context = {'form': form}
    
    if request.method == 'POST':
        form = MyUserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit='')
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, 'You have successfully Register.')
            return redirect('meetup-index')
        else:
            messages.error(request, form.errors)
    return render(request, 'meetup/register.html', context)

#logout view
class LogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, " You have successfully logged Out")
        return super().dispatch(request, *args, **kwargs)
    
        
# index site

def index(request):
    search =request.GET.get('search') if request.GET.get('search') !=None else '' # search meetup
    todayDate = datetime.date.today()
    meetups = Meetup.objects.filter(                      # meetup object in model   
        Q(description__icontains=search)|
        Q(title__icontains=search)
    ).order_by('?')[:6]
    count =meetups.count()
    testimonials=Testimonial.objects.all().order_by('?')
    context = {
        'meetups': meetups,
        'count': count,
        'today': todayDate,
        'testimonials': testimonials,
    }
    return render(request, 'meetup/index.html', context)


# Events
def event(request):
    search =request.GET.get('search') if request.GET.get('search') !=None else '' # search meetup
    todayDate = datetime.date.today()
    meetups = Meetup.objects.filter(                      # meetup object in model   
        Q(description__icontains=search)|
        Q(title__icontains=search)
    )
    count =meetups.count()
    paginated=Paginator(Meetup.objects.all().order_by('-to_date'), 6)
    page=request.GET.get('page') #get requested page number from the 
    meetup=paginated.get_page(page)
    context = {
        'meetups': meetups,
        'count': count,
        'today': todayDate,
        'meetup': meetup,
    }
    return render(request, 'meetup/event.html', context)


# User meetups
@login_required
def user_meetups(request, pk):
    search=request.GET.get('search') if request.GET.get('search') != None else ''
    user_meetup=Meetup.objects.order_by('-title')
    user_meetup=Meetup.objects.filter(user=pk)
    
    
    meetups=user_meetup.filter(
        Q(title__icontains=search)|
        Q(location_name__icontains=search)
    )
    counts = meetups.count()
    
    if request.method == "POST":
        form=TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully commented on our Event Meetup')
            return redirect('/') 
    else:
        form=TestimonialForm()
    context={
        'meetups':meetups,
        'counts':counts,
        'form':form,
    }
    return render(request, 'meetup/user_meetup.html', context)
    

# to view a meetup
def meetup_details(request, meetup_slug):
    selected_meetup =Meetup.objects.get(slug =meetup_slug)    # getting slug data from model(Meetup.objects)
    if request.method=='GET':
        participantForm=ParticipantForm() 
    else:
        participantForm = ParticipantForm(request.POST)
        if participantForm.is_valid():
            paticipant=participantForm.save()
            selected_meetup.participant.add(paticipant)
            # messages.success(request, 'Join request submitted successfully.')
            return redirect('confirm-reg')
        else:
            messages.error(request, 'Invalid form submission.')
            messages.error(request, participantForm.errors)
            
    participants=selected_meetup.participant.all()
    speakers=selected_meetup.meetup_speakers.all()
    count = participants.count()
    context={
        'meetup': selected_meetup,
        'form':participantForm,
        'participants': participants,
        'count': count,
        'speakers': speakers,
        
    }
    return render(request, 'meetup/meetup_details.html', context)

# comfirming Registration for adding participant
@login_required
def confirmReg(request):
    messages.success(request, 'You have successfully Joined.')
    return render(request, 'meetup/confirm_reg.html')


#Upcoming meetups
def upcoming_meetup(request):
    search= request.GET.get('search') if request.GET.get('search')  != None else ''
    meetups = Meetup.objects.filter(activate=True)
    todayDate = datetime.date.today()
    
    meetups=meetups.filter(
        Q(title__icontains=search)|
        Q(location__name__icontains=search)|
        Q(from_date__icontains=search)|
        Q(to_date__icontains=search)
    )
    meetups=meetups.order_by('-meetup_date')
    counts=meetups.count()
    
    context ={
        'todayDate': todayDate,
        'meetups': meetups,
        'counts': counts, 
    }
    return render(request, 'meetup/upcoming_meetup.html', context)


# Creating a meetup
class MeetupCreate(SuccessMessageMixin, CreateView):
    model = Meetup 
    form_class = UseMeetupForm
    # exclude=[]
    success_url = reverse_lazy('meetup-index')
    template_name = 'meetup/meetup_form.html'
    success_message= "Meetup has been created successfully"
    def form_valid(self, form):
        form.instance.user = self.request.user
        for i in punctuation:
            form.instance.title = form.instance.title.replace(i, ' ')
        form.instance.slug = form.instance.title.replace(' ', '-')
        return super(MeetupCreate, self).form_valid(form)
          

    

# update meetup
class MeetupUpdate(SuccessMessageMixin, UpdateView):
    model = Meetup
    form_class = UseMeetupForm
    template_name = "meetup/meetup_form.html"
    success_url = reverse_lazy('meetup-index')
    success_message = "meetup is successfully updated"
    
    def form_isvalid(self, form):   #validate the form
        form.instance.user = self.request.user      #the user instance e.g previous data to be updated
        return super(MeetupUpdate, self).form_valid(form)
 
        
# To delete a meetup using class base view(CBV)

class MeetupDelete(DeleteView):
    model = Meetup
    context_object_name = 'meetup'
    template_name = 'meetup/meetup_delete.html'
    success_url = reverse_lazy('meetup-index')
    
    def form_valid(self, form):
        messages.success(self.request, "The Meetup was deleted successfully.")
        return super(MeetupDelete,self).form_valid(form)
    


###--SPEAKER---######

# add speaker
@login_required
def add_speaker(request, pk):
    selected_meetup = Meetup.objects.get(id=pk)  #using ORM(oject relational mapper) to get data from the database
    if request.method=='GET':
        add_speaker_form = SpeakerForm()
    else:
        add_speaker_form = SpeakerForm(request.POST, request.FILES)
    
    if add_speaker_form.is_valid():     #check if the speaker_form is valid 
        add_speaker_form.instance.meetup_name=selected_meetup.title
        speaker=add_speaker_form.save()
        selected_meetup.meetup_speakers.add(speaker)
        messages.success(request, 'successfully Added speaker.')
        return redirect('meetup-index')
    context ={
        'form':add_speaker_form,
        'meetup': selected_meetup,
        'meetup_found':True,
        'page':'add'
    }
    return render(request, 'meetup/add_speaker.html',context)

# user speaker
@login_required
def user_speaker(request, userid):
    search = request.GET.get('search') if request.GET.get('search') != None else ''  #request.GET.get to get a particular data
    
    user_speakers=Speaker.objects.order_by('-id').filter(user=userid)
    speakers = user_speakers.filter(
        
        Q(name__icontains=search)|
        Q(meetup_name__icontains=search)
    )
    counts= user_speakers.count()
    context ={
        'speakers': speakers,
        'count': counts
        
    }
    return render(request, 'meetup/user-speaker.html',context)

# view speaker
@login_required
def speaker_details(request, meetupid):
    meetup = Meetup.objects.get(id=meetupid)
    speakers=meetup.meetup_speakers.all().order_by('-id')
    count =speakers.count()
    context ={
        'meetup': meetup,
        'speakers': speakers,
        'counts': count
    }
    return render(request, 'meetup/speaker_detail.html', context)


# # update speaker
@login_required
def update_speaker(request, pk):
    speaker=Speaker.objects.get(id=pk)
    if request.method =='POST':
        form=SpeakerForm(request.POST,request.FILES, instance=speaker)
        if form.is_valid():
            form.save()
            messages.success(request, 'Speaker updated successfully.')
        return redirect('/')
    else:
        form=SpeakerForm(instance=speaker)
    context={
        'form': form, 
    }
    return render(request, 'meetup/update_speaker.html', context)

# Delete speaker
@login_required
def delete_speaker(request, pk):
    speaker=Speaker.objects.get(id=pk)
    if request.method=='POST':
        speaker.delete()
        messages.info(request, 'Speaker has been deleted.')
        return redirect('/')
    context={'speaker':speaker,}
    return render(request, 'meetup/delete_speaker.html',context) 
    
# particpant
@login_required
def participants(request, meetupid):
    meetup = Meetup.objects.get(id=meetupid)
    participant=meetup.participant.all().order_by('-id')
    count = participant.count()
    context ={
        'meetup': meetup,
        'participants': participant,
        'counts': count,
    }
    return render(request, 'meetup/participant.html', context)


def testimonial(request):
    testimonials=Testimonial.objects.all().order_by('?')
    context={
        'testimonials': testimonials
    }
    return render(request, 'meetup/testimonial.html',context)

# def comments(request):
    # if request.method == "POST":
    #     form=TestimonialForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'You have successfully commented on our Event Meetup')
    #         return redirect('/') 
    # else:
    #     form=TestimonialForm()
    
    # context={
    #     'form':form
    # }
    # return render(request,'meetup/add_comment.html', context)
    
    
    
def contact(request):
    if request.method == "POST":
        form=ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message']
            }
            message = '\n'.join(body.values())
            try:
                send_mail(subject, message, 'djangocozy@gmail.com', ['djangocozy@gmail.com'])
                messages.success(request, 'A Mail has been sent successfully')
            except BadHeaderError:
                return HttpResponse('Inavlid header found') 
            return redirect('/')
    else:
        form=ContactForm()
    
    return render(request, 'meetup/contact.html', {'form':form})


def success(request):
    return render(request, 'meetup/contact_success.html')



def profile(request):
    return render(request, 'meetup/profile.html')

def profile_update(request):
    if request.method == "POST":
        form=ProfileUpdateForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('user_profile')
    else:
        form=ProfileUpdateForm(instance=request.user)
    context={
        'form': form
    }
    return render(request, 'meetup/edit_profile.html', context)

def app_404(request):
    return render(request, 'meetup/404.html')
