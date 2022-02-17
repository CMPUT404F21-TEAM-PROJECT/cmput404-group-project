from django.urls import path
from . import views

urlpatterns = [
  path('authors/', views.route_multiple_authors, name='Add Author'),
  path('authors/<str:id>/', views.route_single_author, name='Change Author'),
  path('authors/<str:id>/followers/', views.route_multiple_followers, name='Get Followers'),
  path('authors/<str:id>/followers/<str:f_id>', views.route_single_follower, name='Manage Follower'),
]