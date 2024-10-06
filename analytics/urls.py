from django.urls import path
from .views import index, analytics
urlpatterns = [
    path('', index , name='index'),
    path('analytics/', analytics, name='analytics')
]