from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Author, Post
from datetime import datetime
import copy, base64, os

# Author Mock Data

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

# Create your tests here.
class AuthorTestCase(TestCase):
    def setUp(self):
        Author.objects.create(id="test_author_id")

    def test_author_default_values(self):
        author = Author.objects.get(id="test_author_id")
        self.assertEqual(author.id, "test_author_id")

class AuthorEndpointTestCase(APITestCase):
    def test_add_author(self):
        url = '/service/authors/'
        # Add an author
        response = self.client.post(url, author1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check for correct attributes
        savedAuthor = Author.objects.get(id=author1["id"])
        self.assertEqual(savedAuthor.url, author1["url"])
        self.assertEqual(savedAuthor.host, author1["host"])
        self.assertEqual(savedAuthor.displayName, author1["displayName"])
        self.assertEqual(savedAuthor.github, author1["github"])
        self.assertEqual(savedAuthor.profileImage, author1["profileImage"])
        self.assertEqual(savedAuthor.password, author1["password"])

    def test_get_multiple_authors(self):
        url = '/service/authors/'

        # Add 2 authors
        self.client.post(url, author1, format='json')
        self.client.post(url, author2, format='json')

        # Get multiple authors
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure 2 authors returned
        responseJson = response.json()
        self.assertEqual(len(responseJson['items']), 2)

    def test_delete_author(self):
        addUrl = '/service/authors/'
        deleteUrl = '/service/authors/' + author1["id"] + '/'

        # Add an author
        response =self.client.post(addUrl, author1, format='json')

        # Delete the author
        response = self.client.delete(deleteUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the author was deleted
        try:
            Author.objects.get(id=author1["id"])

            # If the get does not raise an error, that means the deleted author was found
            self.assertEqual("Deleted author was found", "after being deleted")
        except:
            return

    def test_update_author(self):
        addUrl = '/service/authors/'
        updateUrl = '/service/authors/' + author1["id"] + '/'

        # Add an author
        self.client.post(addUrl, author1, format='json')

        # Update the author
        author1Updated = copy.deepcopy(author2)
        author1Updated["id"] = author1["id"]
        response = self.client.post(updateUrl, author1Updated, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for updated attributes
        savedAuthor = Author.objects.get(id=author1["id"])
        self.assertEqual(savedAuthor.url, author1Updated["url"])
        self.assertEqual(savedAuthor.host, author1Updated["host"])
        self.assertEqual(savedAuthor.displayName, author1Updated["displayName"])
        self.assertEqual(savedAuthor.github, author1Updated["github"])
        self.assertEqual(savedAuthor.profileImage, author1Updated["profileImage"])
        self.assertEqual(savedAuthor.password, author1Updated["password"])

    def test_get_single_author(self):
        getUrl = '/service/authors/' + author1["id"] + '/'
        addUrl = '/service/authors/'

        # Add an author
        self.client.post(addUrl, author1, format='json')

        # Get the author
        response = self.client.get(getUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for correct attributes
        responseJson = response.json()
        self.assertEqual(responseJson["id"], author1["id"])
        self.assertEqual(responseJson["url"], author1["url"])
        self.assertEqual(responseJson["host"], author1["host"])
        self.assertEqual(responseJson["displayName"], author1["displayName"])
        self.assertEqual(responseJson["github"], author1["github"])
        self.assertEqual(responseJson["profileImage"], author1["profileImage"])
        self.assertEqual(responseJson["password"], author1["password"])

