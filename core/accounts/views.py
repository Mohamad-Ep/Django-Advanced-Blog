from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from .tasks import get_send_email
import requests

# __________________________________________________________


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")


# __________________________________________________________


def send_Email(request):
    get_send_email.delay()
    return HttpResponse("<h1>send Email</h1>")


# __________________________________________________________

# def test_mock(request):
#     response = requests.get("https://5ef37103-7b47-486b-8557-106c12475492.mock.pstmn.io/test/delay/5")
#     return JsonResponse(response.json())
# __________________________________________________________
