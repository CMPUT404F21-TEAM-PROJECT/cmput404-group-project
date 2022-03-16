from cgitb import text
import uuid, jwt, json
from rest_framework import status
from django.test import TestCase
from api.models import Author, Post, Comment, User
from rest_framework.test import APITestCase, APIClient
from datetime import datetime
from django.utils import timezone


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

# Post Mock Data

textPostPlain = {
    "id": "81111111-1111-1111-1111-111111111111",
    "title":"a",
    "contentType":"text/plain",
    "content":"a",
    "description":"a",
    "visibility":"PUBLIC",
    "published":"2022-01-11T09:26:03.478039-07:00",
    "source":"a",
    "origin":"a",
    "categories":"b",
    "unlisted":False,
    "viewableBy":'',
}

# Comment Mock Data 

commentPost1 = {
    "id": "81111111-1111-1111-1111-111111111111",
    "contentType":"text/html",
    "comment":"My First Comment"
}
commentPost2 = {
    "id": "91111111-1111-1111-1111-111111111111",
    "contentType":"text/html",
    "comment":"My Second Comment"
}

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


class CommentEndpointTestCase(APITestCase):
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
        textPostPlain["author"] = user1Id

        # Update authors
        updateUrl1 = '/authors/' + author1["id"] + '/'
        updateUrl2 = '/authors/' + author2["id"] + '/'
        
        cls.client.post(updateUrl1, author1, format='json')
        cls.client.post(updateUrl2, author2, format='json')

    def test_create_comment_endpoint(self):
        """
            Test that a user is able to make comments for a post once it is created
        """
        loginUrl = "/login/"
        # Authenticate Current User
        valid_response = self.client.post(loginUrl, user1, format='json')
        access_token = valid_response.data
        jwt_id = jwt.decode(access_token['jwt'], key='secret', algorithms=['HS256'])["id"]
        # Create a new post using the jwt_id
        postsUrl = '/authors/' + jwt_id + '/posts/'
        response = self.client.post(postsUrl, textPostPlain, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(postsUrl, textPostPlain, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)   
        data = response.json()

        commentPost1["post_id"] = data["items"][0]['id']
        # Create a new comment using the created post id
        commentUrl = '/authors/' + jwt_id + '/posts/' + commentPost1["post_id"] +'/comments/'
        response = self.client.post(commentUrl, commentPost1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_comments_endpoint(self):
        """
            Test that a user is able to make and get multiple comments from one post
        """
        loginUrl = "/login/"
        # Authenticate Current User
        valid_response = self.client.post(loginUrl, user1, format='json')
        access_token = valid_response.data
        jwt_id = jwt.decode(access_token['jwt'], key='secret', algorithms=['HS256'])["id"]
        # Create a new post using the jwt_id
        postsUrl = '/authors/' + jwt_id + '/posts/'
        response = self.client.post(postsUrl, textPostPlain, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(postsUrl, textPostPlain, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        commentPost1["post_id"] = data["items"][0]['id']
        commentPost2["post_id"] = data["items"][0]['id']
        # Create two comment objects
        commentUrl = '/authors/' + jwt_id + '/posts/' + commentPost1["post_id"] +'/comments/'
        response = self.client.post(commentUrl, commentPost1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(commentUrl, commentPost2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(commentUrl, commentPost1, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        responseJson = response.json()
        self.assertEqual(responseJson["items"][1]['comment'], commentPost1["comment"])
        self.assertEqual(responseJson["items"][0]['comment'], commentPost2["comment"])

    def test_get_single_comment_endpoint(self):
        """
            Test that a user is able to view a single comment from a post
        """
        loginUrl = "/login/"
        # Authenticate Current User
        valid_response = self.client.post(loginUrl, user1, format='json')
        access_token = valid_response.data
        jwt_id = jwt.decode(access_token['jwt'], key='secret', algorithms=['HS256'])["id"]
        # Create a new post using the jwt_id
        postsUrl = '/authors/' + jwt_id + '/posts/'
        response = self.client.post(postsUrl, textPostPlain, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(postsUrl, textPostPlain, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        commentPost1["post_id"] = data["items"][0]['id']
        commentPost2["post_id"] = data["items"][0]['id']
        commentUrl = '/authors/' + jwt_id + '/posts/' + commentPost1["post_id"] +'/comments/'
        # Create two comment objects
        response = self.client.post(commentUrl, commentPost1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(commentUrl, commentPost2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the second comment's data and verify it
        singleCommentUrl = '/authors/' + jwt_id + '/posts/' + commentPost2["post_id"] +'/comments/' + commentPost2["id"] + '/'
        response = self.client.get(singleCommentUrl, commentPost2, format='json')
        responseJson = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(responseJson["id"], commentPost2["id"])
        self.assertEqual(responseJson["contentType"], commentPost2["contentType"])
        self.assertEqual(responseJson["comment"], commentPost2["comment"])

    def test_update_comment_endpoint(self):
        """
            Test that a user is only able to edit their comments and not others
        """
        loginUrl = "/login/"
        logoutUrl = "/logout/"
        # Authenticate Current User
        valid_response = self.client.post(loginUrl, user1, format='json')
        access_token = valid_response.data
        jwt_id = jwt.decode(access_token['jwt'], key='secret', algorithms=['HS256'])["id"]
        # Create a new post using the jwt_id
        postsUrl = '/authors/' + jwt_id + '/posts/'
        response = self.client.post(postsUrl, textPostPlain, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(postsUrl, textPostPlain, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        commentPost1["post_id"] = data["items"][0]['id']
        commentUrl = '/authors/' + jwt_id + '/posts/' + commentPost1["post_id"] +'/comments/'
        # Create a new comment object
        response = self.client.post(commentUrl, commentPost1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Update the first comment and verify it
        singleCommentUrl = '/authors/' + jwt_id + '/posts/' + commentPost1["post_id"] +'/comments/' + commentPost1["id"] + '/'
        response = self.client.get(singleCommentUrl, commentPost1, format='json')
        responseJson = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(responseJson["id"], commentPost1["id"])
        self.assertEqual(responseJson["contentType"], commentPost1["contentType"])
        self.assertEqual(responseJson["comment"], commentPost1["comment"])
        # Update the first comment with new data and verify
        commentPost1["comment"] = "Test Update"
        response = self.client.put(singleCommentUrl, commentPost1, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(singleCommentUrl, commentPost1, format='json')
        responseJson = response.json()
        self.assertEqual(responseJson["id"], commentPost1["id"])
        self.assertEqual(responseJson["contentType"], commentPost1["contentType"])
        self.assertEqual(responseJson["comment"], commentPost1["comment"])
        # Logout the current user and login a new user 
        self.client.post(logoutUrl, user1, format='json')
        self.client.post(loginUrl, user2, format='json')
        commentPost1["comment"] = "Invalid Update"
        # Try to update the previous comment by user1 as user2
        response = self.client.put(singleCommentUrl, commentPost1, format='json')
        # Assert that it returns a 401 unauthorized status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_comment_endpoint(self):
        """
            Test that a user is only able to delete their comments and not others
        """
        loginUrl = "/login/"
        logoutUrl = "/logout/"
        # Authenticate Current User
        valid_response = self.client.post(loginUrl, user1, format='json')
        access_token = valid_response.data
        jwt_id = jwt.decode(access_token['jwt'], key='secret', algorithms=['HS256'])["id"]
        # Create a new post using the jwt_id
        postsUrl = '/authors/' + jwt_id + '/posts/'
        response = self.client.post(postsUrl, textPostPlain, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(postsUrl, textPostPlain, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        commentPost1["post_id"] = data["items"][0]['id']
        commentPost2["post_id"] = data["items"][0]['id']
        comment1Url = '/authors/' + jwt_id + '/posts/' + commentPost1["post_id"] +'/comments/'
        comment2Url = '/authors/' + jwt_id + '/posts/' + commentPost2["post_id"] +'/comments/'
        # Create a two new comment object
        response = self.client.post(comment1Url, commentPost1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(comment2Url, commentPost2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Delete the first comment and verify it
        singleComment1Url = '/authors/' + jwt_id + '/posts/' + commentPost1["post_id"] +'/comments/' + commentPost1["id"] + '/'
        singleComment2Url = '/authors/' + jwt_id + '/posts/' + commentPost2["post_id"] +'/comments/' + commentPost2["id"] + '/'
        response = self.client.delete(singleComment1Url, commentPost1, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Try and get the first comment again, check for a 404 status code
        response = self.client.get(singleComment1Url, commentPost1, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Logout the current user and login a new user 
        self.client.post(logoutUrl, user1, format='json')
        self.client.post(loginUrl, user2, format='json')
        # Try to delete the second comment by user1 as user2
        response = self.client.put(singleComment2Url, commentPost2, format='json')
        # Assert that it returns a 401 unauthorized status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)