from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('generate/', generate, name='generate'),
    path('search/', SearchView.as_view(), name='search')
]