from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result/', views.result, name='result'),
    path('result/detail/', views.detail, name='detail'),
    path('query_complete/', views.query_complete, name='query_complete')
]