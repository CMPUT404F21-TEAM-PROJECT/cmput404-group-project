from django.urls import path
from . import views

urlpatterns = [
  path('authors/', views.route_multiple_authors, name='Multiple Authors'),
  path('authors/<str:author_id>/', views.route_single_author, name='Single Author'),
  path('authors/<str:author_id>/posts/', views.route_multiple_posts, name='Multiple Posts'),
  path('authors/<str:author_id>/posts/<str:post_id>/', views.route_single_post, name='Single Post'),
  path('authors/<str:author_id>/posts/<str:post_id>/image/', views.route_single_image_post, name='Single Image Post'),
]