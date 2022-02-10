from django.urls import path
from . import views

urlpatterns = [
  path('authors', views.add_author, name='Add Author'),
  path('authors/<str:id>', views.change_author, name='Change Author')
]