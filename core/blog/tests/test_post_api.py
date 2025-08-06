import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User,Profile
from blog.models import Category
from datetime import datetime
# __________________________________________________________

# fixure function
@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def user_object():
    user = User.objects.create_user(email='hsasdfg10@gmail.com',password='Aa123456@',is_verficated=True,is_active=True)
    return user

# -----------------------------------

@pytest.mark.django_db
class TestPostApi:
    
    def test_get_post_api_response_200_status(self,api_client):
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == 200


    def test_post_api_response_201_status(self,api_client,user_object):
        url = reverse("blog:api-v1:post-list")
        # profile_obj = Profile.objects.create(user=user_object)
        category_obj = Category.objects.create(name='test')
        data = {
            'title':'test',
            'status':True,
            'category':category_obj.id,
        }
        
        # api_client.force_login(user=user_object)
        api_client.force_authenticate(user=user_object)
        response = api_client.post(url,data)
        assert response.status_code == 201

# __________________________________________________________

