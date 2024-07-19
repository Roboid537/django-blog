from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APITestCase

from users.models import CustomUser
from .models import Post, Comment



class ModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test data for the Model test case."""
        cls.user = CustomUser.objects.create_user(username='testuser',
                                                  email='testuser@mail.com',
                                                  password='testpassword')
        cls.post = Post.objects.create(title="Post with Comments",
                                        author=cls.user,
                                        content="Some content")


class ViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up common test data."""
        cls.user1 = CustomUser.objects.create_user(username='user1',
                                                   email='user1@mail.com',
                                                    password='password1')
        cls.user2 = CustomUser.objects.create_user(username='user2',
                                                   email='user2@mail.com',
                                                   password='password2')
        cls.post1 = Post.objects.create(title="Post 1",
                                        author=cls.user1,
                                        content="Content 1")
        cls.post2 = Post.objects.create(title="Post 2",
                                        author=cls.user2,
                                        content="Content 2")
        cls.comment1 = Comment.objects.create(post=cls.post1,
                                              author=cls.user1,
                                              content="Comment 1")
        cls.comment2 = Comment.objects.create(post=cls.post1,
                                              author=cls.user2,
                                              content="Comment 2")


class PostModelTest(ModelTest):

    def test_post_creation(self):
        """Test creating a new post."""
        post = Post.objects.create(
            title="Test Post",
            author=self.user,
            content="This is a test post content."
        )
        self.assertEqual(str(post), "Test Post by testuser")
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "This is a test post content.")
        self.assertEqual(post.author, self.user)

    def test_post_ordering(self):
        """Verify posts are ordered by creation date (descending)."""
        post1 = Post.objects.create(title="Post 1",
                                    author=self.user,
                                    content="Content 1")
        post2 = Post.objects.create(title="Post 2",
                                    author=self.user,
                                    content="Content 2")
        posts = Post.objects.all()
        self.assertEqual(posts[0], post1)
        self.assertEqual(posts[1], post2)

    def test_post_likes(self):
        """Test adding and removing likes from a post."""
        post = Post.objects.create(title="Liked Post",
                                   author=self.user,
                                   content="Liked Content")
        user2 = CustomUser.objects.create_user(username='user2',
                                               email='user2@mail.com',
                                               password='password2')

        # Add likes
        post.likes.add(self.user, user2)
        self.assertEqual(post.likes.count(), 2)

        # Remove a like
        post.likes.remove(self.user)
        self.assertEqual(post.likes.count(), 1)


class CommentModelTest(ModelTest):

    def test_comment_creation(self):
        """Test creating a new comment."""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="This is a test comment."
        )
        self.assertEqual(str(comment), "This is a test comme by testuser")
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, "This is a test comment.")

    def test_comment_ordering(self):
        """Verify comments are ordered by creation date (descending)."""
        comment1 = Comment.objects.create(post=self.post,
                                           author=self.user,
                                           content="Comment 1")
        comment2 = Comment.objects.create(post=self.post,
                                          author=self.user,
                                          content="Comment 2")
        comments = self.post.comments.all()
        self.assertEqual(comments[0], comment1)
        self.assertEqual(comments[1], comment2)


class PostViewSetTests(ViewTest):

    def test_get_post_list(self):
        """Test retrieving the list of posts."""
        url = reverse('posts:post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 2)

    def test_get_single_post(self):
        """Test retrieving a single post."""
        url = reverse('posts:post-detail', kwargs={'pk': self.post1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.post1.pk)

    def test_create_post(self):
        """Test creating a new post (requires authentication)."""
        url = reverse('posts:post-list')
        data = {'title': 'New Post', 'content': 'New post content'}
        self.client.force_authenticate(user=self.user1)  # Authenticate
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(response.data['title'], 'New Post')

    def test_update_post(self):
        """Test updating an existing post (author only)."""
        url = reverse('posts:post-detail', kwargs={'pk': self.post1.pk})
        data = {'title': 'Updated Title', 'content': 'Updated content'}
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get(pk=self.post1.pk).title, 'Updated Title')

        # Try updating as another user
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LikePostAPIViewTests(ViewTest):

    def test_like_post(self):
        """Test liking a post."""
        url = reverse('posts:like-post', kwargs={'pk': self.post1.pk})
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user1, self.post1.likes.all())

    def test_unlike_post(self):
        """Test unliking a post."""
        url = reverse('posts:like-post', kwargs={'pk': self.post1.pk})
        self.client.force_authenticate(user=self.user1)
        self.client.get(url)  # Like the post first
        response = self.client.get(url)  # Unlike
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.user1, self.post1.likes.all())
