import uuid
from django.test import TestCase
from api.models import Author, Post, Comment, User
from datetime import datetime
from django.utils import timezone

class CommentTestCase(TestCase):

    def setUp(self):
        self.id = uuid.uuid4()
        self.post_id = uuid.uuid4()
        self.comment_id = uuid.uuid4()
        self.user = User.objects.create(id=self.id)
        self.author = Author.objects.create(id=self.user)
        self.post = Post.objects.create(id=self.post_id, author=self.author, published=datetime.now())
        Comment.objects.create(id=self.comment_id, post_id=self.post, author=self.author, published=timezone.now())

    def test_comment_default_values(self):
        comment = Comment.objects.get(id=self.comment_id)
        self.assertEqual(comment.id, self.comment_id)
        self.assertEqual(comment.author, self.author)