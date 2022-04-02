from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Author, FollowRequest, User
from datetime import datetime
import copy, base64, os
import uuid
import environ

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


class FollowersEndpointTestCase(APITestCase):
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
        self.object = Author.objects.get(id=author1["id"])
        self.actor = Author.objects.get(id=author2["id"])

        # make actor a follower of object
        FollowRequest.objects.create(summary='blah',
                                     actor=self.actor,
                                     object=self.object,
                                     accepted=True)

    def test_get_followers(self):
        """Test GET request for getting a list of followers."""
        url = self.object.id + "/followers/"
        url = url.replace(env("LOCAL_HOST"), "")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        responseJson = response.json()
        self.assertEqual('followers', responseJson['type'])
        self.assertEqual(self.actor.id, responseJson['items'][0]['id'])
        self.assertEqual(len(responseJson['items']), 1)
    
    def test_get_following(self):
        """Test GET request for getting a list of people you follow."""
        url = self.actor.id + '/following/'
        url = url.replace(env("LOCAL_HOST"), "")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        responseJson = response.json()
        self.assertEqual('following', responseJson['type'])
        self.assertEqual(self.object.id, responseJson['items'][0]['id'])
        self.assertEqual(len(responseJson['items']), 1)
        

    def test_remove_follower(self):
        """Test DELETE request for removing a follower."""
        loginUrl = "/login/"
        self.client.post(loginUrl, user1, format='json')

        url = '/authors/' + self.object.id + '/followers/' + self.actor.id + "/"
        url = url.replace(env("LOCAL_HOST")+"/authors/", "")

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the follow request was deleted
        self.assertEqual(0, len(FollowRequest.objects.all()))

    def test_add_follower(self):
        """Test PUT request for adding a follower (accepting a follow request)."""
        loginUrl = "/login/"
        self.client.post(loginUrl, user2, format='json')

        # object has already sent a follow request to actor
        FollowRequest.objects.create(summary='blah',
                                     actor=self.object,
                                     object=self.actor)

        url = '/authors/' + self.actor.id + '/followers/' + self.object.id + "/"
        url = url.replace(env("LOCAL_HOST")+"/authors/", "")

        response = self.client.put(url)
        fr = FollowRequest.objects.get(actor=self.object,
                                       object=self.actor)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(fr.accepted)

    def test_get_follower(self):
        """Test GET request for checking if someone is a follower."""
        url = '/authors/' + self.object.id + '/followers/' + self.actor.id + "/"
        url = url.replace(env("LOCAL_HOST")+"/authors/", "")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # testing a non follower
        url = '/authors/' + self.object.id + '/followers/' + self.object.id + "/"
        url = url.replace(env("LOCAL_HOST")+"/authors/", "")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.json().get('message', None), None)
