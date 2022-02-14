from django.urls import path
from . import views

urlpatterns = [
  path('authors/', views.route_multiple_authors, name='Add Author'),
  path('authors/<str:id>/', views.route_single_author, name='Change Author'),
  path('authors/<str:authorID>/inbox/', views.send_like, name="Send Like"),
  path('authors/<str:authorID>/posts/<str:postID>/likes', views.get_post_likes, name="Get Post Like"),
  path('authors/<str:authorID>/posts/<str:postID>/comments/<str:commentID>/likes', views.get_comment_likes, name="Get Comment Likes"),
  path('authors/<str:authorID>/liked', views.get_author_likes, name="Get Author's Likes")

]

