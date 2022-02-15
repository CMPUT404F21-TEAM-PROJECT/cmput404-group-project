from django.urls import path
from . import views

urlpatterns = [
  path('authors/', views.route_multiple_authors, name='Multiple Authors'),
  path('authors/<str:id>/', views.route_single_author, name='Single Author')
]