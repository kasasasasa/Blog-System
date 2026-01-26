from django.urls import path
from . import views

app_name = 'blogauth'

urlpatterns = [
    path('login/', views.blogin, name='login'),
    path('logout/', views.blogout, name='logout'),
    path('register/', views.register, name='register'),
    path('captcha/', views.send_email_captcha, name='email_captcha'),
]