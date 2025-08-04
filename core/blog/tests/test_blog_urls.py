from django.test import TestCase,SimpleTestCase
from django.urls import reverse,resolve
from ..views import IndexView,PostList,PostDetailsView
# __________________________________________________________

class TestUrl(SimpleTestCase):                           # باید اول کلاس کلمه Test درج شود
    def test_blog_index_url_resolve(self):              # حتما باید اولش کلمه test بخورد
        url = reverse('blog:cbv-index')
        self.assertEqual(resolve(url).func.view_class,IndexView)
        
    def test_blog_list_url_resolve(self):        
        url = reverse('blog:posts')
        self.assertEqual(resolve(url).func.view_class,PostList)
        
    def test_blog_details_url_resolve(self):        
        url = reverse('blog:post_details',kwargs={'pk':1})
        self.assertEqual(resolve(url).func.view_class,PostDetailsView)

# __________________________________________________________
