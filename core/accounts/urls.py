from django.urls import path
from . import views

# __________________________________________________________

app_name = 'accounts'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
 
]

# __________________________________________________________