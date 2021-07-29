
from django.urls import path
from parseapp import views
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('get_keywords/', views.get_keywords, name='get_keywords'),
    path('<str:keyword>/' , views.keyWord, name= "get_keyword"),
]