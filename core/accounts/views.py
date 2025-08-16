from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from .tasks import get_send_email
import requests
from django.core.cache import cache
from django.views.decorators.cache import cache_page

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
#     if cache.get('test_delay_api') is None:
#         response = requests.get("https://5ef37103-7b47-486b-8557-106c12475492.mock.pstmn.io/test/delay/5")
#         data = response.json()
#         cache.set('test_delay_api',data,600)
#         # cache.delete('test_delay_api')
#     return JsonResponse(cache.get('test_delay_api'),safe=False)
# __________________________________________________________


@cache_page(timeout=700, key_prefix="deplay_api")  # cache='test'
def test_mock(request):
    response = requests.get(
        "https://5ef37103-7b47-486b-8557-106c12475492.mock.pstmn.io/test/delay/5"
    )
    data = response.json()
    return JsonResponse(data, safe=False)


# __________________________________________________________
