from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('error_detection/', views.error_detection, name='error_detection'),
    path('orientation/', views.orientation, name='orientation'),    
    path('number_fluency/', views.number_fluency, name='number_fluency'),    
    path('word_rules/', views.word_rules, name='word_rules'),    
    path('deductive_reasoning/', views.deductive_reasoning, name='deductive_reasoning'),
    path('reasoning_categories/', views.reasoning_categories, name='reasoning_categories'),
]
