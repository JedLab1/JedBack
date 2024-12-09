from django.urls import path
from . import views

urlpatterns = [
    path('activity/', views.create_activity, name='generate_expression'),
]
