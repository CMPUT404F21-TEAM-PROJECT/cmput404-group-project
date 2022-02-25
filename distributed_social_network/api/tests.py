from shutil import register_unpack_format
import uuid
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Author, Post, Comment, User, Like
from django.utils import timezone
from datetime import datetime
import copy, base64, os, json
from django.db.models import Q
from http.cookies import SimpleCookie

# User Mock Data

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
    "id": "41111111-1111-1111-1111-111111111111",
    "title":"textPostTitle1",
    "contentType":"text/plain",
    "content":"textPostContent1",
    "description":"textDescription1",
    "visibility":"PUBLIC",
    "published":"2022-01-10",
    "source":"textSource1",
    "origin":"textOrigin1",
    "categories":"textCategories1",
    "unlisted":False
}

textPostMarkdown = {
    "id": "51111111-1111-1111-1111-111111111111",
    "title":"textPostTitle2",
    "contentType":"text/markdown",
    "content":"textPostContent2",
    "description":"textDescription2",
    "visibility":"PUBLIC",
    "published":"2022-01-11",
    "source":"textSource2",
    "origin":"textOrigin2",
    "categories":"textCategories2",
    "unlisted":False
}

os.chdir(os.path.dirname(__file__))
imagePostPng = {
    "id": "11111111-1111-1111-1111-111111111111",
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
    "id": "21111111-1111-1111-1111-111111111111",
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
    "id": "31111111-1111-1111-1111-111111111111",
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

comment = {
    "author": "testAuthor",
    "comment": "testComment",
    "contentType": "testContentType",
    "published": "testPublished",
    "id": "testID"
}
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
        self.id = uuid.uuid4()
        self.user = User.objects.create(id=self.id)
        Author.objects.create(id=self.user)

    def test_author_default_values(self):
        author = Author.objects.get(id=self.id)
        self.assertEqual(author.id, self.user)


class PostTestCase(TestCase):
    def setUp(self):
        self.id = uuid.uuid4()
        self.post_id = uuid.uuid4()
        self.user = User.objects.create(id=self.id)
        self.author = Author.objects.create(id=self.user)
        self.post = Post.objects.create(id=self.post_id, author=self.author, published=datetime.now())

    def test_author_default_values(self):
        post = Post.objects.get(id=self.post_id)
        self.assertEqual(post.id, self.post_id)
        self.assertEqual(post.author, self.author)


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
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        # Create 2 new users if they don't already exist
        registerUrl = "/service/register/"
        cls.client.post(registerUrl, user1, format='json')
        cls.client.post(registerUrl, user2, format='json')
        
        # Save their ids
        user1Id = str(User.objects.get(username=user1["username"]).id)
        user2Id = str(User.objects.get(username=user2["username"]).id)
        author1["id"] = user1Id
        author2["id"] = user2Id
        user1["id"] = user1Id
        user2["id"] = user2Id
        imagePostBase64["author"] = user1Id
        imagePostPng["author"] = user1Id
        imagePostJpeg["author"] = user1Id

        # Update authors
        updateUrl1 = '/service/authors/' + author1["id"] + '/'
        updateUrl2 = '/service/authors/' + author2["id"] + '/'
        
        cls.client.post(updateUrl1, author1, format='json')
        cls.client.post(updateUrl2, author2, format='json')

    def test_get_multiple_authors(self):
        # Log in as user1
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user1, format='json')

        url = '/service/authors/'

        # Get multiple authors
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure 2 authors returned
        responseJson = response.json()
        self.assertEqual(len(responseJson['items']), 2)

    def test_update_author(self):
        # Log in as user1
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user1, format='json')

        updateUrl = '/service/authors/' + author1["id"] + '/'

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

    def test_get_single_author(self):
        # Log in as user1
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user1, format='json')

        getUrl = '/service/authors/' + author1["id"] + '/'

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

class PostEndpointTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        # Create 2 new users if they don't already exist
        registerUrl = "/service/register/"
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
        textPostMarkdown["author"] = user1Id
        imagePostBase64["author"] = user1Id
        imagePostPng["author"] = user1Id
        imagePostJpeg["author"] = user1Id

        # Update authors
        updateUrl1 = '/service/authors/' + author1["id"] + '/'
        updateUrl2 = '/service/authors/' + author2["id"] + '/'
        cls.client.post(updateUrl1, author1, format='json')
        cls.client.post(updateUrl2, author2, format='json')

    def test_get_text_post(self):

        # Log in as user1
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user1, format='json')

        postUrl = '/service/authors/' + author1["id"] + '/posts/' + textPostPlain["id"] + '/'

        # Add a text post
        response = self.client.put(postUrl, textPostPlain, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the text post
        response = self.client.get(postUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for correct attributes
        responseJson = response.json()
        self.assertEqual(responseJson["id"], textPostPlain["id"])
        self.assertEqual(responseJson["author"], textPostPlain["author"])
        self.assertEqual(responseJson["title"], textPostPlain["title"])
        self.assertEqual(responseJson["contentType"], textPostPlain["contentType"])
        self.assertEqual(responseJson["content"], textPostPlain["content"])
        self.assertEqual(responseJson["description"], textPostPlain["description"])
        self.assertEqual(responseJson["visibility"], textPostPlain["visibility"])
        self.assertEqual(responseJson["published"], textPostPlain["published"])
        self.assertEqual(responseJson["source"], textPostPlain["source"])
        self.assertEqual(responseJson["origin"], textPostPlain["origin"])
        self.assertEqual(responseJson["categories"], textPostPlain["categories"])
        self.assertEqual(responseJson["unlisted"], textPostPlain["unlisted"])

    def test_get_multiple_posts(self):
        # This test posts 2 posts of different types to the multiple posts url
        # It then gets both posts using the multiple posts url
        # It then verifies that the id of the post has changed and the content has not
        
        # Log in as user1
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user1, format='json')

        postsUrl = '/service/authors/' + author1["id"] + '/posts/'

        # Add 2 text posts
        response = self.client.post(postsUrl, textPostPlain, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(postsUrl, textPostMarkdown, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get multiple posts
        response = self.client.get(postsUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure 2 posts returned
        responseJson = response.json()
        self.assertEqual(len(responseJson['items']), 2)

        # Since Pagenation can return random order, determine which is which
        if responseJson['items'][0]['content'] == textPostPlain['content']:
            plainPost = responseJson['items'][0]
            markdownPost = responseJson['items'][1]
        else:
            plainPost = responseJson['items'][1]
            markdownPost = responseJson['items'][0]
        
        # Assert the id has changed but the content has not
        self.assertNotEqual(plainPost['id'], textPostPlain['id'])
        self.assertEqual(plainPost['content'], textPostPlain['content'])
        self.assertNotEqual(markdownPost['id'], textPostMarkdown['id'])
        self.assertEqual(markdownPost['content'], textPostMarkdown['content'])

    def test_get_image_post_jpeg(self):
        # Log in as user1
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user1, format='json')
        
        addPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostJpeg["id"] + '/'
        getPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostJpeg["id"] + '/image/'

        # Add an image post
        response = self.client.put(addPostUrl, imagePostJpeg, format='json', )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the image post
        response = self.client.get(getPostUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the image matches the posted image
        self.assertEqual(response.content, open(os.getcwd() + "/testing_media/test.jpeg", 'rb').read())

    def test_get_image_post_png(self):
        # Log in as user1
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user1, format='json')

        addPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostPng["id"] + '/'
        getPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostPng["id"] + '/image/'

        # Add an image post
        response = self.client.put(addPostUrl, imagePostPng, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the image post
        response = self.client.get(getPostUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the image matches the posted image
        self.assertEqual(response.content, open(os.getcwd() + "/testing_media/test.png", 'rb').read())

    def test_get_image_post_base64(self):
        # Log in as user1
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user1, format='json')

        addPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostBase64["id"] + '/'
        getPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostBase64["id"] + '/image/'

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
        self.assertEqual(savedLike.author, postLike1["author"]) 
        self.assertEqual(savedLike.object, postLike1["object"])


    def test_get_post_likes(self):
        postUrl =  "/service/authors/{}/inbox/".format(postAuthor)
        getUrl = "/service/authors/{0}/posts/{1}/likes".format(postAuthor, postID)

        #Add likes 
        self.client.post(postUrl, postLike1, format="json")
        self.client.post(postUrl, postLike2, format="json")

        response = self.client.get(getUrl, format="json")
        likes = response.json()["items"] #List of likes
    

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
        likes = response.json()["items"] #List of likes

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
        likes = response.json()["items"] #List of likes

        self.assertEqual(response.status_code, status.HTTP_200_OK) #Check that request returned 200 code
        self.assertEqual(len(likes), 2) #Check that 2 likes were returned 

        #Check that the items returned are the mock likes
        self.assertTrue(postLike1 in likes) 
        self.assertTrue(commentLike1 in likes) 

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

