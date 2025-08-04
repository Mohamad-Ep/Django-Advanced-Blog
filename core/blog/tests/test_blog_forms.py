from django.test import SimpleTestCase,TestCase
from ..forms import PostForm
from ..models import Category
from accounts.models import Profile,User
# __________________________________________________________

class TestPostForm(TestCase):
    def test_post_form_with_valid_data(self):
        user = User.objects.create_user(email='example@yahoo.com',password='123456')
        category_obj = Category.objects.create(name='deram')
        author_obj = Profile.objects.get(user=user)
        
        post_form = PostForm(data={
            'title':'test',
            'status':True,
            'author':author_obj,
            'category':category_obj
        })
        
        self.assertTrue(post_form.is_valid())
        
    def test_post_form_with_not_valid_data(self):
        post_form = PostForm(data={})
           
        self.assertFalse(post_form.is_valid()) 
# __________________________________________________________
