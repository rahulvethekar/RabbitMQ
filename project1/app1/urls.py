from django.urls import path
from .views import MiddlewareCallApi
urlpatterns =[
    path('api/send_request/' ,MiddlewareCallApi.as_view(),name = 'send_request'), #test it on postman.
]