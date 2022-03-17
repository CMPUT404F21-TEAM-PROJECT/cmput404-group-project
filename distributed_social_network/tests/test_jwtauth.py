import uuid, jwt
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Author, User, Post
from datetime import datetime

# User Mock Data

user1 = {
    "username":"user1",
    "password":"password1"
}
# Author Mock Data

author1 = {
    "url":"testingUrl1",
    "host":"testingHost1",
    "displayName":"testingDisplayName1",
    "github":"testingGithub1",
    "profileImage":"testingProfileImage1"
}

# Post Mock Data

textPostPlain = {
    "id": "41111111-1111-1111-1111-111111111111",
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

class UserTestCase(TestCase):

    def setUp(self):
        self.id = uuid.uuid4()
        self.post_id = uuid.uuid4()
        self.user = User.objects.create(id=self.id)
        self.author = Author.objects.create(id=self.user)
        self.post = Post.objects.create(id=self.post_id, author=self.author, published=datetime.now())

    def test_user_default_values(self):
        user = User.objects.get(id=self.id)
        self.assertEqual(user.id, self.user.id)

class UserEndpointTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        # Create 2 new users if they don't already exist
        registerUrl = "/register/"
        cls.client.post(registerUrl, user1, format='json')
        
        # Save their ids
        user1Id = str(User.objects.get(username=user1["username"]).id)
        author1["id"] = user1Id
        user1["id"] = user1Id
        textPostPlain["author"] = user1Id

        # Update authors
        updateUrl1 = '/authors/' + author1["id"] + '/'
        cls.client.post(updateUrl1, author1, format='json')
    
    def test_login_endpoint(self):
        """
            Test that a valid user is able to login and receive a jwt access token
            Also tests that an invalid login will result in either a 401 or 404 if user is found but wrong credentials or not found respectively
        """
        loginUrl = "/login/"
        # Authenticate Current User
        valid_response = self.client.post(loginUrl, user1, format='json')
        access_token = valid_response.data
        jwt_id = jwt.decode(access_token['jwt'], key='secret', algorithms=['HS256'])["id"]
        user_id = User.objects.all().filter(username = user1["username"]).first().id
        self.assertTrue(str(jwt_id) == str(user_id))
        self.assertTrue(valid_response.status_code == 201)
        not_found_response = self.client.post(loginUrl, {"username": "notFound", "password": "invalid"})
        self.assertTrue(not_found_response.status_code == 404)
        unauthenticated_response = self.client.post(loginUrl, {"username": "user1", "password": "invalid"})
        self.assertTrue(unauthenticated_response.status_code == 401)

    def test_logout_endpoint(self):
        """
            Test that a user is able to login and make a new post, check that they cannot make another one when logging out
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
        # Log user out
        self.client.post(logoutUrl, user1, format='json')
        # Assert that a post request when unauthenticated results in a jwt error, (invalid token)
        try:
            response = self.client.post(postsUrl, textPostPlain, format='json')
        except Exception as e:
            self.assertTrue(type(e) == jwt.DecodeError)
