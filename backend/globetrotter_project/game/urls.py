from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Additional API endpoints can be added here.
]
