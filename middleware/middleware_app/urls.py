from django.urls import path
from middleware_app.views import ConsumeApiView

urlpatterns =[
    path('api/middleware/',ConsumeApiView.as_view(),name='middleware'),
]
