from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
  path('register/', views.create_new_user, name="Create New User"),
  path('login/', views.login_user, name="Log User In"),
  path('get-user/', views.get_user, name="Get User Info"),
  path('logout/', views.log_user_out, name="Log User Out"),
  path('authors/', views.route_multiple_authors, name='Multiple Authors'),
  path('authors/<str:author_id>/', views.route_single_author, name='Single Author'),
  path('authors/<str:author_id>/posts/', views.route_multiple_posts, name='Multiple Posts'),
  path('authors/<str:author_id>/posts/<str:post_id>/', views.route_single_post, name='Single Post'),
  path('authors/<str:author_id>/posts/<str:post_id>/image/', views.route_single_image_post, name='Single Image Post'),
  path('authors/<str:author_id>/followers/', views.route_multiple_followers, name='Get Followers'),
  path('authors/<str:author_id>/following/', views.route_multiple_following, name='Get Following'),
  path('authors/<str:author_id>/followers/<str:follower_id>/', views.route_single_follower, name='Manage Follower'),
  path('authors/<str:authorID>/posts/<str:postID>/likes/', views.get_post_likes, name="Get Post Like"),
  path('authors/<str:authorID>/posts/<str:postID>/comments/<str:commentID>/likes/', views.get_comment_likes, name="Get Comment Likes"),
  path('authors/<str:authorID>/liked/', views.get_author_likes, name="Get Author's Likes"),
  path('authors/<str:author_id>/posts/<str:post_id>/comments/', views.route_multiple_comments, name='Multiple Comments'),
  path('authors/<str:author_id>/posts/<str:post_id>/comments/<uuid:comment_id>/', views.route_single_comment, name='Single Comment'),
  path('authors/<str:author_id>/inbox/', views.route_inbox, name='Inbox'),
]
