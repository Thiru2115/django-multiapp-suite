from django.urls import path
from . import views

app_name = 'ai_hub'

urlpatterns = [
    path('', views.hub_home, name='hub_home'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('summarizer/', views.summarizer_view, name='summarizer'),
    path('image-generator/', views.image_generator_view, name='image_generator'),
]
