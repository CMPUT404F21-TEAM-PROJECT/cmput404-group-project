from django.urls import path
from . import views

urlpatterns = [
  path('authors/', views.route_multiple_authors, name='Multiple Authors'),
  path('authors/<str:id>/', views.route_single_author, name='Single Author')
  path('authors/<str:id>/posts/', views.route_multiple_posts, name='Multiple Posts')
  path('authors/<str:id>/posts/<str:id>/', views.route_single_post, name='Single Post')
]