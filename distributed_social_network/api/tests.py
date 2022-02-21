from django.test import TestCase
from .models import Author, Post
from datetime import datetime

# Create your tests here.
class AuthorTestCase(TestCase):
    def setUp(self):
        Author.objects.create(id="test_author_id")

    def test_author_default_values(self):
        author = Author.objects.get(id="test_author_id")
        self.assertEqual(author.id, "test_author_id")


class PostTestCase(TestCase):
    def setUp(self):
        author = Author.objects.create(id="test_author_id")
        post = Post.objects.create(id="test_post_id", author=author, published=datetime.now())

    def test_author_default_values(self):
        post = Post.objects.get(id="test_post_id")
        self.assertEqual(post.id, "test_post_id")
        self.assertEqual(post.author.id, "test_author_id")
