from urllib import response
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Post, Like
from datetime import datetime
import copy, base64, os
from django.db.models import Q




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

# Post Mock Data

os.chdir(os.path.dirname(__file__))
imagePostPng = {
    "id": "imageId1",
    "author":"testingId1",
    "title":"imageTitle1",
    "contentType":"image/png;base64",
    "content":base64.b64encode(open(os.getcwd() + "/testing_media/test.png", 'rb').read()),
    "description":"imageDescription1",
    "visibility":"PUBLIC",
    "published":"2022-01-10",
    "source":"imageSource1",
    "origin":"imageOrigin1",
    "categories":"imageCategories1",
    "unlisted":False
}

imagePostJpeg = {
    "id": "imageId1",
    "author":"testingId1",
    "title":"imageTitle1",
    "contentType":"image/jpeg;base64",
    "content":base64.b64encode(open(os.getcwd() + "/testing_media/test.jpeg", 'rb').read()),
    "description":"imageDescription1",
    "visibility":"PUBLIC",
    "published":"2022-01-10",
    "source":"imageSource1",
    "origin":"imageOrigin1",
    "categories":"imageCategories1",
    "unlisted":False
}

imagePostBase64 = {
    "id": "imageId1",
    "author":"testingId1",
    "title":"imageTitle1",
    "contentType":"application/base64",
    "content":base64.b64encode(open(os.getcwd() + "/testing_media/test.png", 'rb').read()),
    "description":"imageDescription1",
    "visibility":"PUBLIC",
    "published":"2022-01-10",
    "source":"imageSource1",
    "origin":"imageOrigin1",
    "categories":"imageCategories1",
    "unlisted":False
}

######### Start Like Mock Data #########
PORT = "5438"
HOST = "127.0.0.1"
author1ID = author1["id"]
author2ID = author2["id"]
post = imagePostPng
postID = post["id"]
postAuthor = post["author"]
comment = None #TODO change once comment is merged
commentID = comment["id"]

#Like left by author1 on post
postLike1 = {
   "summary": "postLike1Summary",
   "author": author1,
   "object": "http://{0}:{1}/authors/{2}/posts/{3}".format(HOST, PORT, postAuthor, postID)
}

#Like left by author2 on post
postLike2 = {
    "summary": "postLike2Summary",
    "author": author2,
    "object": "http://{0}:{1}/authors/{2}/posts/{3}".format(HOST, PORT, postAuthor, postID)
}


#Like left by author1 on comment
commentLike1 = {
    "summary": "commentLike1Summary",
    "author": author1,
    "object": "http://{0}:{1}/authors/{2}/posts/{3}/comments/{4}".format(HOST, PORT, postAuthor, postID, commentID)
}

#Like left by author2 on comment
commentLike2 = {
    "summary": "commentLike2Summary",
    "author": author2,
    "object": "http://{0}:{1}/authors/{2}/posts/{3}/comments/{4}".format(HOST, PORT, postAuthor, postID, commentID)
}

######### End Like Mock Data #########

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


class LikeTestCase(TestCase):
    def setUp(self):
        author = Author.objects.create(id="test_author_id")
        Like.objects.create(summary="test_like_summary", author=author, object="test_like_object") 

    def test_like_default_values(self):
        author = Author.objects.get(id="test_author_id")
        like = Like.objects.get(Q(author=author) & Q(object="test_like_object"))
        self.assertEqual(like.summary, "test_like_summary")
        self.assertEqual(like.author, author)
        self.assertEqual(like.object, "test_like_object")


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

class PostEndpointTestCase(APITestCase):
    def test_get_image_post_jpeg(self):
        addAuthorUrl = '/service/authors/'
        addPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostJpeg["id"] + '/'
        getPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostJpeg["id"] + '/image/'

        # Add an author
        response = self.client.post(addAuthorUrl, author1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Add an image post
        response = self.client.put(addPostUrl, imagePostJpeg, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the image post
        response = self.client.get(getPostUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the image matches the posted image
        self.assertEqual(response.content, open(os.getcwd() + "/testing_media/test.jpeg", 'rb').read())

    def test_get_image_post_png(self):
        addAuthorUrl = '/service/authors/'
        addPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostPng["id"] + '/'
        getPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostPng["id"] + '/image/'

        # Add an author
        response = self.client.post(addAuthorUrl, author1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Add an image post
        response = self.client.put(addPostUrl, imagePostPng, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the image post
        response = self.client.get(getPostUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the image matches the posted image
        self.assertEqual(response.content, open(os.getcwd() + "/testing_media/test.png", 'rb').read())

    def test_get_image_post_base64(self):
        addAuthorUrl = '/service/authors/'
        addPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostBase64["id"] + '/'
        getPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostBase64["id"] + '/image/'

        # Add an author
        response = self.client.post(addAuthorUrl, author1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Add an image post
        response = self.client.put(addPostUrl, imagePostBase64, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the image post
        response = self.client.get(getPostUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the image matches the posted image
        self.assertEqual(response.content, open(os.getcwd() + "/testing_media/test.png", 'rb').read())


class LikeEndpointTestCase(APITestCase):
    def test_send_like(self):
        url = "/service/authors/{}/inbox/".format(postAuthor)
        object = "http://{0}:{1}/authors/{2}/posts/{3}".format(HOST, PORT, postAuthor, postID)
        response = self.client.post(url, postLike1, format="json")
        savedLike = Like.objects.get(Q(author=author1) & Q(object=object))
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) #Check that request returned 201 code
        
        #Check that all fields are correct
        self.assertEqual(savedLike.summary, postLike1["summary"])
        self.assertEqual(savedLike.author, postLike1["author"]) #TODO see if this works
        self.assertEqual(savedLike.object, postLike1["object"])


    def test_get_post_likes(self):
        postUrl =  "/service/authors/{}/inbox/".format(postAuthor)
        getUrl = "/service/authors/{0}/posts/{1}/likes".format(postAuthor, postID)

        #Add likes 
        self.client.post(postUrl, postLike1, format="json")
        self.client.post(postUrl, postLike2, format="json")

        response = self.client.get(getUrl, format="json")
        likes = response.json()["items"] #TODO check how multiple likes are represented in json
    

        self.assertEqual(response.status_code, status.HTTP_200_OK) #Check that request returned 200 code
        self.assertEqual(len(likes), 2) #Check that 2 likes were returned 
        
        #Check that the items returned are the mock likes
        self.assertTrue(postLike1 in likes) 
        self.assertTrue(postLike2 in likes) 
        

    def test_get_comment_likes(self):
        postUrl = "/service/authors/{}/inbox/".format(postAuthor)
        getUrl = "/service/authors/{0}/posts/{1}/comments/{2}/likes".format(postAuthor, postID, commentID)

        #Add likes 
        self.client.post(postUrl, commentLike1, format="json")
        self.client.post(postUrl, commentLike2, format="json")

        response = self.client.get(getUrl, format="json")
        likes = response.json()["items"] #TODO check how multiple likes are represented in json

        self.assertEqual(response.status_code, status.HTTP_200_OK) #Check that request returned 200 code
        self.assertEqual(len(likes), 2) #Check that 2 likes were returned 
        
        #Check that the items returned are the mock likes
        self.assertTrue(commentLike1 in likes) 
        self.assertTrue(commentLike2 in likes) 

    def test_get_author_likes(self):
        postUrl = "/service/authors/{}/inbox/".format(postAuthor)
        getUrl = "/service/authors/{}/liked".format(postAuthor)

        #Add likes 
        self.client.post(postUrl, postLike1, format="json")
        self.client.post(postUrl, commentLike1, format="json")

        response = self.client.get(getUrl, format="json")
        likes = response.json()["items"] #TODO check how multiple likes are represented in json

        self.assertEqual(response.status_code, status.HTTP_200_OK) #Check that request returned 200 code
        self.assertEqual(len(likes), 2) #Check that 2 likes were returned 

        #Check that the items returned are the mock likes
        self.assertTrue(postLike1 in likes) 
        self.assertTrue(commentLike1 in likes) 