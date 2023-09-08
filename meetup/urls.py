from django.urls import path
from . import views
from .views import MeetupDelete,MeetupCreate,MeetupUpdate, SpeakerUpdate, LogoutView
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
    path('update-speaker/<int:pk>', SpeakerUpdate.as_view(), name='update-speaker'),
    path('speaker-details/<int:meetupid>', views.speaker_details, name='speaker-detail'),
    path('participants/<int:meetupid>', views.participants, name='view-participants'),
    path('meetup-update/<int:pk>',MeetupUpdate.as_view(), name='meetup_update'),
    path('meetup-delete/<int:pk>',MeetupDelete.as_view(), name='meetup_delete'),
    path('password-reset', PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-complete', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
