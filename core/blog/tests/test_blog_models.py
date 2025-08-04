from django.test import SimpleTestCase,TestCase
from ..forms import PostForm
from ..models import Category
from accounts.models import Profile,User
from blog.models import Post
# __________________________________________________________

class TestPostModel(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(email='sfrgh@gmail.com',password='123456')
        self.profile_obj = Profile.objects.create(user=self.user)
        self.category_obj = Category.objects.create(name='test')
    
    def test_pot_model_with_valid_data(self):

        post = Post.objects.create(
            title = 'test',
            author = self.profile_obj,
            category = self.category_obj,
        )
        
        self.assertTrue(Post.objects.get_or_create(pk=post.id))
        self.assertEqual(post.title,'test')
# __________________________________________________________