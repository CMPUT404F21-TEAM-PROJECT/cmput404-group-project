from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Author, FollowRequest, Inbox, Post
from datetime import datetime
import copy, base64, os

# Mock Data

author1 = {
    "id":"testingId1",
    "url":"testingUrl1",
    "host":"testingHost1",
    "displayName":"testingDisplayName1",
    "github":"testingGithub1",
    "profileImage":"testingProfileImage1",
    "password":"testingPassword1",
}

author2 = {
    "id":"testingId2",
    "url":"testingUrl2",
    "host":"testingHost2",
    "displayName":"testingDisplayName2",
    "github":"testingGithub2",
    "profileImage":"testingProfileImage2",
    "password":"testingPassword2",
}

user1 = {
    "username":"user1",
    "password":"password1"
}

user2 = {
    "username":"user2",
    "password":"password2"
}

post1 = {
    "type":"post",
    "id": "postId1",
    "author":"testingId2",
    "title":"title1",
    "contentType":"text/plain",
    "content":"blah",
    "description":"test post",
    "visibility":"PUBLIC",
    "published":"2022-01-10",
    "source":"source1",
    "origin":"origin1",
    "categories":"categories1",
    "unlisted":False
}

post2 = {
    "type":"post",
    "id": "postId2",
    "author":"testingId2",
    "title":"title1",
    "contentType":"text/plain",
    "content":"blah",
    "description":"test post",
    "visibility":"PUBLIC",
    "published":"2022-01-10",
    "source":"source1",
    "origin":"origin1",
    "categories":"categories1",
    "unlisted":False
}

follow_request = {
    "type":"follow",
    "summary":"blah",
}

# Create your tests here.
class InboxTestCase(TestCase):
    def setUp(self):
        author = Author.objects.create(id="test_author_id")
        Inbox.objects.create(author=author)

    def test_inbox_default_values(self):
        author = Author.objects.get(id="test_author_id")
        inbox = Inbox.objects.get(author=author)
        self.assertEqual(inbox.author, author)

class InboxEndpointTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # register author 
        cls.client = APIClient()
        registerUrl = "/service/register/"
        cls.client.post(registerUrl, user1, format='json')
        cls.client.post(registerUrl, user2, format='json')
        user1Id = str(self.author.id)
        author1["id"] = user1Id
        updateUrl1 = '/service/authors/' + author1["id"] + '/'
        cls.client.post(updateUrl1, author1, format='json')
        user2Id = str(self.actor.id)
        author2["id"] = user2Id
        updateUrl2 = '/service/authors/' + author2["id"] + '/'
        cls.client.post(updateUrl2, author2, format='json')

        # # remove when auth stuff is merged
        # Author.objects.create(**author1)
        # Author.objects.create(**author2)

    def setUp(self):
        self.author = Author.objects.get(username=user1["username"])
        self.actor = Author.objects.get(username=user2["username"])

        # create inbox and populate with a post
        self.inbox = Inbox.objects.create(author=self.author)
        self.inbox.posts.add(Post.objects.create(**post1))


    def test_get_inbox(self):
        """Test GET request for getting an inbox."""
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user1, format='json')
        
        url = '/service/authors/' + author1["id"] + '/inbox/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        responseJson = response.json()
        self.assertEqual(self.author.id, responseJson['author'])
        self.assertEqual(len(responseJson['items']), 1)

    def test_get_paginated_inbox(self):
        """Test GET request for getting a paginated inbox."""
        # loginUrl = "/service/login/"
        # self.client.post(loginUrl, user1, format='json')
        pass # TODO

    def test_clear_inbox(self):
        """Test DELETE request for clearing an inbox."""
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user1, format='json')

        url = '/service/authors/' + author1["id"] + '/inbox/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the inbox was cleared
        inbox = Inbox.objects.get(author=self.author)
        self.assertEqual(0, len(inbox.posts.all()))
        self.assertEqual(0, len(inbox.likes.all()))
        self.assertEqual(0, len(inbox.follow_requests.all()))

    def test_add_local_post(self):
        """Test POST request for sending a local post to an inbox."""
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user2, format='json')

        url = '/service/authors/' + author1["id"] + '/inbox/'

        response = self.client.post(url, post2, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        inbox = Inbox.objects.get(author=self.author)
        self.assertEqual(2, len(inbox.posts.all()))

    def test_add_local_follow(self):
        """Test POST request for sending a follow request from a local author to an inbox."""
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user2, format='json')

        url = '/service/authors/' + author1["id"] + '/inbox/'

        response = self.client.post(url, follow_request, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        inbox = Inbox.objects.get(author=self.author)
        self.assertEqual(1, len(inbox.follow_requests.all()))

    def test_add_local_like(self):
        """Test POST request for sending a like for a local post/comment to an inbox."""
        pass

    # TODO: implement for part 2
    # def test_add_remote_post(self):
    #     """Test POST request for sending a remote post to an inbox."""
    #     pass

    # def test_add_remote_follow(self):
    #     """Test POST request for sending a follow request from a remote author to an inbox."""
    #     pass

    # def test_add_remote_like(self):
    #     """Test POST request for sending a like for a remote post/comment to an inbox."""
    #     pass
