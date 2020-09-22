from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup', sign_up, name='sign-up')
]