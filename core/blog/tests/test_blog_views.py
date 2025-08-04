from django.test import TestCase,Client
from django.urls import reverse
from ..models import Category
from accounts.models import Profile,User
# __________________________________________________________

class TestBlogView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='sfrgh12@gmail.com',password='1234567895')
        self.profile_obj = Profile.objects.create(user=self.user)
        self.category_obj = Category.objects.create(name='test')
        
    def test_blog_index_url_response_successful(self):
        url = reverse('blog:cbv-index')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code,200)
        self.assertTrue(str(response.content).find('index'))
        self.assertTemplateUsed(response,template_name='blog/index.html')
        
    # def test_blog_post_create_login_response(self):           # Error for force_login
    #     self.client.force_login(self.user)
    #     url = reverse('blog:post_create')
    #     response = self.client.get(url)     
    #     self.assertEqual(response.status_code,200)
        
    def test_blog_post_create_anonymous_response(self):
        url = reverse('blog:post_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code,302)
# __________________________________________________________