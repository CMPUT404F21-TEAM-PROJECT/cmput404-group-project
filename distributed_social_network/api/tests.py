import uuid
from django.test import TestCase
from .models import Author, Post, Comment
from django.utils import timezone
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


class CommentTestCase(TestCase):

    uuid = uuid.uuid4()

    def setUp(self):
        author = Author.objects.create(id="test_author_id")
        post = Post.objects.create(id="test_post_id", author=author, published=datetime.now())
        Comment.objects.create(id=self.uuid, post_id=post, author=author, published=timezone.now())

    def test_comment_default_values(self):
        comment = Comment.objects.get(id=self.uuid)
        self.assertEqual(comment.post_id.id, "test_post_id")
        self.assertEqual(comment.author.id, "test_author_id")