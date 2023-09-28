from django.urls import path
from . import views
from .views import MeetupDelete,MeetupCreate,MeetupUpdate, LogoutView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView,PasswordResetDoneView,PasswordResetCompleteView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.index, name='meetup-index'),
    path('meetup-events/', views.event, name='meetup-event'),
    path('meetup/<slug:meetup_slug>', views.meetup_details, name='meetup_detail'),
    path('login/', views.Login, name='meetup_login'),
    path('register/', views.Register, name='meetup_register'),
    path('confirm-registration/', views.confirmReg, name='confirm-reg'),
    path('logout/', LogoutView.as_view(next_page='meetup_login'), name='meetup_logout'),
    path('meetup-create/',login_required(MeetupCreate.as_view()), name='meetup_create'),
    path('upcoming_meetup/', views.upcoming_meetup, name='upcoming_meetup'),
    path('user-meetup/<int:pk>', views.user_meetups, name='user-meetup'),
    path('add-speaker/<int:pk>', views.add_speaker, name='add-speaker'),
    path('delete-speaker/<int:pk>', views.delete_speaker, name='delete_speaker'),
    path('update-speaker/<int:pk>', views.update_speaker, name='update_speaker'),
    path('speaker-details/<int:meetupid>', views.speaker_details, name='speaker-detail'),
    path('participants/<int:meetupid>', views.participants, name='view-participants'),
    path('meetup-update/<int:pk>',login_required(MeetupUpdate.as_view()), name='meetup_update'),
    path('meetup-delete/<int:pk>',login_required(MeetupDelete.as_view()), name='meetup_delete'),
    path('password-reset/', login_required(PasswordResetView.as_view(template_name='meetup/password_reset.html')), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='meetup/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name='meetup/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-complete', PasswordResetCompleteView.as_view(template_name='meetup/password_reset_complete.html'), name='password_reset_complete'),
    
    path('meetup-testimonails/', views.testimonial, name='meetup_testimonial'),
    # path('meetup-comments', views.comments, name='meetup_comment'),
    path('contact', views.contact, name='meetup_contact'),
    path('profile', views.profile, name='user_profile'),
    path('update/profile', views.profile_update, name='meetup_profile_update'),
    path('404', views.app_404, name='meetup_404'),
   

]
