from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Author, FollowRequest, Like, Inbox, Post, User, Comment
from datetime import datetime
import copy, base64, os
import uuid, environ
from django.db.models import Q

env = environ.Env()
environ.Env.read_env()

# Mock Data

user1 = {
    "username":"user1",
    "password":"password1"
}

user2 = {
    "username":"user2",
    "password":"password2"
}

# Author Mock Data

author1 = {
    "url":"testingUrl1",
    "host":"testingHost1",
    "displayName":"testingDisplayName1",
    "github":"testingGithub1",
    "profileImage":"testingProfileImage1"
}

author2 = {
    "url":"testingUrl2",
    "host":"testingHost2",
    "displayName":"testingDisplayName2",
    "github":"testingGithub2",
    "profileImage":"testingProfileImage2"
}

post1 = {
    "id": str(uuid.uuid4()),
    "title":"textPostTitle1",
    "contentType":"text/plain",
    "content":"textPostContent1",
    "description":"textDescription1",
    "visibility":"PUBLIC",
    "published":"2022-01-11T09:26:03.478039-07:00",
    "source":"textSource1",
    "origin":"textOrigin1",
    "categories":"textCategories1",
    "unlisted":False,
    "viewableBy":'',
}

post2 = {
    "id": str(uuid.uuid4()),
    "title":"textPostTitle2",
    "contentType":"text/markdown",
    "content":"textPostContent2",
    "description":"textDescription2",
    "visibility":"PUBLIC",
    "published":"2022-01-11T09:26:03.478039-07:00",
    "source":"textSource2",
    "origin":"textOrigin2",
    "categories":"textCategories2",
    "unlisted":False,
    "viewableBy":'',
}

follow_request = {
    "type":"follow",
    "summary":"blah",
}

postLike1 = {
    "type": "Like",
    "summary": "postLike1Summary",
}

commentPost1 = {
    "contentType":"text/html",
    "comment":"My First Comment",
    "published":"2022-01-11T09:26:03.478039-07:00",
}

PORT = "5438"
HOST = "127.0.0.1"

# Create your tests here.
class InboxEndpointTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        # Create 2 new users if they don't already exist
        registerUrl = "/register/"
        cls.client.post(registerUrl, user1, format='json')
        cls.client.post(registerUrl, user2, format='json')
        
        # Save their ids
        user1Id = str(User.objects.get(username=user1["username"]).id)
        user2Id = str(User.objects.get(username=user2["username"]).id)
        author1["id"] = user1Id
        author2["id"] = user2Id
        user1["id"] = user1Id
        user2["id"] = user2Id

    def setUp(self):
        self.author = Author.objects.get(id=author1["id"])
        self.actor = Author.objects.get(id=author2["id"])

        # Update post authors
        post1["author"] = self.actor
        post2["author"] = self.actor
        commentPost1["author"] = self.author

        # get inbox and populate with a post
        self.inbox = Inbox.objects.get(author=self.author.id)
        postUrl = author1["id"].replace(env("LOCAL_HOST"), "") + "posts/" + post1['id'] + "/"
        response = self.client.put(postUrl, post1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        commentPost1["post_id"] = response.json()["id"]
        self.inbox.posts.add(Post.objects.get(id=response.json()["id"]))

        # make author follow actor (so actor can send stuff to author's inbox)
        FollowRequest.objects.create(summary='blah',
                                     actor=self.author,
                                     object=self.actor,
                                     accepted=True)
        
        # make another post that will be added to the inbox in a test
        postUrl = author1["id"].replace(env("LOCAL_HOST"), "") + "posts/" + post2['id'] + "/"
        response = self.client.put(postUrl, post2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        commentUrl = commentPost1["post_id"].replace(env("LOCAL_HOST"), "") + '/comments/'
        response = self.client.post(commentUrl, commentPost1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_inbox(self):
        """Test GET request for getting an inbox."""
        loginUrl = "/login/"
        self.client.post(loginUrl, user1, format='json')
        
        url = author1["id"].replace(env("LOCAL_HOST"), "") + '/inbox/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        responseJson = response.json()
        self.assertEqual(str(self.author.id.id), responseJson['author'])
        self.assertEqual(len(responseJson['items']), 1)

    def test_get_paginated_inbox(self):
        """Test GET request for getting a paginated inbox."""
        # loginUrl = "/login/"
        # self.client.post(loginUrl, user1, format='json')
        pass # TODO

    def test_clear_inbox(self):
        """Test DELETE request for clearing an inbox."""
        loginUrl = "/login/"
        self.client.post(loginUrl, user1, format='json')

        url = author1["id"].replace(env("LOCAL_HOST"), "") + '/inbox/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the inbox was cleared
        inbox = Inbox.objects.get(author=self.author)
        self.assertEqual(0, len(inbox.posts.all()))
        self.assertEqual(0, len(inbox.likes.all()))
        self.assertEqual(0, len(inbox.follow_requests.all()))
        self.assertEqual(0, len(inbox.comments.all()))

    def test_add_local_post(self):
        """Test POST request for sending a local post to an inbox."""
        loginUrl = "/login/"
        self.client.post(loginUrl, user2, format='json')

        url = author1["id"].replace(env("LOCAL_HOST"), "") + '/inbox/'

        local_post = post2.copy()
        local_post['type'] = 'post'

        response = self.client.post(url, local_post, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        inbox = Inbox.objects.get(author=self.author)
        self.assertEqual(2, len(inbox.posts.all()))

    def test_add_local_follow(self):
        """Test POST request for sending a follow request from a local author to an inbox."""
        loginUrl = "/login/"
        self.client.post(loginUrl, user2, format='json')

        url = author1["id"].replace(env("LOCAL_HOST"), "") + '/inbox/'

        response = self.client.post(url, follow_request, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        inbox = Inbox.objects.get(author=self.author)
        self.assertEqual(1, len(inbox.follow_requests.all()))
    
    def test_add_local_comment(self):
        """Test POST request for sending a local comment to an inbox."""
         # make actor follow author (so author can send stuff to actor's inbox)
        FollowRequest.objects.create(summary='blah',
                                     actor=self.actor,
                                     object=self.author,
                                     accepted=True)
        loginUrl = "/login/"
        self.client.post(loginUrl, user1, format='json')

        url = author2["id"].replace(env("LOCAL_HOST"), "") + '/inbox/'

        local_comment = commentPost1.copy()
        local_comment['type'] = 'comment'

        response = self.client.post(url, local_comment, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        inbox = Inbox.objects.get(author=self.actor)
        self.assertEqual(1, len(inbox.comments.all()))

    # TODO: Figure out AuthorSerializer() errors
    def test_add_local_like(self):
        """Test POST request for sending a like for a local post/comment to an inbox."""
        # make actor follow author (so author can send stuff to actor's inbox)
        FollowRequest.objects.create(summary='blah',
                                     actor=self.actor,
                                     object=self.author,
                                     accepted=True)
        # Log in as user1
        loginUrl = "/login/"
        self.client.post(loginUrl, user1, format='json')

        url = author1["id"].replace(env("LOCAL_HOST"), "") + '/inbox/'
        # postLike1['object'] = "http://{0}:{1}/authors/{2}/posts/{3}".format(HOST, PORT, author2, post1['id'])
        postLike1['object'] = post1['id']
        response = self.client.post(url, postLike1, format="json") 

        self.assertEqual(response.status_code, status.HTTP_201_CREATED) #Check that request returned 201 code

        savedLike = Like.objects.get(summary="postLike1Summary")
        
        #Check that all fields are correct
        self.assertEqual(savedLike.summary, postLike1["summary"])
        self.assertEqual(savedLike.author, self.author) 
        self.assertEqual(savedLike.object, postLike1["object"])

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
