from django.urls import path
from . import views

urlpatterns = [
    path('api/chat/', views.get_response, name='get_response'),
]
